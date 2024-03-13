### Login function

```mermaid

graph TD
    A[1. Get_token ] --> B[2.Sync With Vs Userinfo]
    B--> C["Mapping Individual package by country"]
    C--> D["3. Check Individual Plan"]
    D -->E[4. Sync Vs Entities with orgs]
    E --> F[5.Get Response data]
    F --> G[Return to Client]
```

### 1. Get_token

```mermaid

graph LR
    A[Get code verifier in redis by code_challenge] --> B[POST - VS API/token by `auth_code + verifier` or `refresh_code`]

```

### 2. Sync With Vs Userinfo

```mermaid

graph LR
    A[ Invoke VS API GET /userinfo by access_token] --> B[Get vs_userinfo ex: user_id/email]
    B --> C["_Upsert Individual User"]

```

### 3. Check Individual Plan

- 個人組織未曾有過 plan,會根據國家給予 30 天的 Plus or Basic Plan
- 如果個人組織已經有存在 plan 則會確定所有方案是否過期,過期則會補一個 Permanent `Basic` Plan

```mermaid

graph LR

    Plan{Individual Org has plan?} -->CheckExpired{Are all plans in the individual organization expired?} --> |Yes|CreatePlan[Create a permanent`Basic` plan]-->Done
    CheckExpired--> |No|Done
    Plan --> |No|Plan_F["Create 30-day `Plus|Basic` Plan"] --> Done
```

### 4. Sync Vs Entities with orgs

```mermaid

graph LR

    Get_entity[Invoke VS API  GET /<:id>/entity] --> Entity_list[Get entity_list ]
    Entity_list --> Upsert_org_for_loop["_Upsert new org (for loop every entity)" ]
    Upsert_org_for_loop--> Insert_entiy_owner_for_loop["_Insert entity owner (for loop every entity)"]


```

### 5.Get Response data

```mermaid

graph LR

    Get_org_list[Get org_list in DB ] --> Get_is_consent["Query for existence in the 'user_consent' table." ]
    --> Get_is_filled_info["Query for 'is_filled_info' in the 'user' table."]

```

### \_Upsert Individual User

```mermaid

graph LR

    In[/input/] --> User{User Exist?}
    User --> |Yes|User_T["Update User first/last name"]
    User --> |No|User_F["Create User"] --> Org
    User_T --> Org["Upsert new org [Individual]"]
```

### \_Upsert new org[Individual/Entity]

```
- Entity:  org_id=entity_id
- Individual: org_id=user_id(normal)/is_individual=True
```

```mermaid

graph LR
    In[/input/] --> O{Organization exist?}
    O --> |not exist|OF["Create organization"]
    O --> |exist|OT["Update organization name" ]
    OF --> PO
    OT --> PO{Personal Organization?}
    PO --> |No|Done
    PO --> |Yes|POT{Has teacher role?}
    POT --> |No|R["Crate teacher role"]
    POT --> |Yes|Done
    R --> Done


```

### \_Insert entity owner

```mermaid

graph LR

    Check_user{role including owner?} --> |Yes|Check_role{Owner role in org?} --> Done
    Check_user--> Done
    Check_role--> |No|role_n["Create a owner role "] --> Done

```

### Request body

- auth_code+code_challenge or refresh_token 二擇一

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

```
{
    "data": {
        "user_id": "str",
        "email": "str",
        "first_name": "str",
        "last_name": "str",
        "organizations": [
            {
                "user_display_name":"",
                "org_id": "",
                "package": "",
                "org_name": "",
                "roles": [
                    "teacher"
                ],
                "package_code": 1,
                "end_date": int|null,
                "student_concurrent":int
            },
        ],
        "individual": {
           "user_display_name": "str",
           "org_id": "str",
           "package": "str",
           "org_name": "Individual",
           "roles": [
                "teacher"
             ],
           "package_code": int,
           "end_date": int/null,
           "student_concurrent":int
        },
        "id_token": "",
        "access_token:"",
        "refresh_token":"",
        "is_filled_info":bool
        "is_consent":bool,
        "country:"",
    }
}
```
