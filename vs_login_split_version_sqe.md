# /vs/auth/login

```mermaid
sequenceDiagram
    participant client as Client
    participant Backend as Backend
    participant vsa as ViewSonic Account
    participant vse as ViewSonic Entity


    client ->> Backend : request /login
    Backend ->> vsa : request token api
    note left of vsa : {oidc_domain}/auth/{api_version}/oidc/token 2.5s
    vsa ->> Backend : access_token, id_token, (refresh token)
    Backend ->> vsa : request user info by access token
    note left of vsa : {oidc_domain}/auth/{api_version}/oidc/userinfo 2.5s
    vsa ->> Backend : user information

    Backend ->> Backend : login status check(is_filled_info/is_consent)
    alt login is success
        Backend ->> client : token, user info, entity info
    else login is fail
        Backend ->> client : error message
    end
```

### Request body

- 兩種形式的 body :

  - auth_code+code_challenge:

  ```
    {
      "code": "string",
      "code_challenge":"",
      "redirect_uri":"",
      "client": "string" APP|WEB,
      }
  ```

  - refresh_token:

  ```
   {
     "refresh_token":"",
     "redirect_uri":"",
     "client": "string" APP|WEB,
   }
  ```

### Response

    {
    "data": {
        "user_id": "str",
        "email": "str",
        "first_name": "str",
        "last_name": "str",
        "id_token": "",
        "access_token":"",
        "refresh_token":"",
        "is_filled_info":bool
        "is_consent":bool,
        "country:"",
    }
    }

### 商業邏輯：

    invoke VS API get token + VS API  get userinfo
    Upsert user_id in user table
    Return token/userinfo/is_counsent/is_filled_info

# POST /vs/organization

```mermaid
sequenceDiagram
    participant client as Client
    participant Backend as Backend
    participant vse as ViewSonic Entity


    client ->> Backend : request /organization
    Backend ->> vse : request entity-info by user id
    note left of vse : {domain}/account/api/{api_version}/account/{user_id}/entity-info 1.3s
    vse ->> Backend : get entity information
    Backend ->> Backend : sync organization information
    Backend ->> client :return organization information

```

### Request

    headers:
    - access_token
    - country

### Response

```

{
  "entity":[
            {
                "user_display_name":"",
                "org_id": "",
                "package": "",
                "org_name": "",
                "package_code": int,
                "role":["owner","teacher"],
                "end_date": int|null,
                "student_concurrent":int
            },{...},
          ],
 "individual":{
            "user_display_name": "str",
            "org_id": "str",
            "package": "str",
            "org_name": "Individual",
            "package_code": int,
            "role":["owner","teacher"],
            "end_date": int/null,
            "student_concurrent":int,
        },
}
```

### 商業邏輯：

    Invoke VS API entity-info
    Upsert organization/user_org/user_role/package/plan tables
    Return organization info
