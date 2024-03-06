# on_teacher_force_logout

- #### Infra

  - [x] Redis
  - [x] RDS

- #### Client

  - [ ] Teacher App
  - [ ] Participant
  - [x] Hub

- #### Server Event Handler

  - data

    ```
      {
        user_id:"",
        org_id:"",
      }
    ```

  - callback
    ```
    None
    ```

- #### Client Event Handler

  - listener: Teacher APP
  - event name: teacher_force_logout
  - channel: the sid of the force_logout user
  - data:

    ```
      {"user_id": ""}
    ```

- ## Flow

  - ### 1. Hub

    ```mermaid
      sequenceDiagram
        autonumber
        participant M as Hub
        participant B as Socket Server
        participant R as Redis
        participant D as RDS
        participant A as Teacher APP

        M->>B: emit teacher_force_logout(user_id,org_id)
        D->>B: get open lesson_id

        alt if open lesson exists
              B->>+D: execute end lesson
        end
        R->>B: set {"force_logout_time":int} to [cooldown:org_{org_id}_user_{user_id}] & TTL 5 mins
        R->>B: get forced logout teacher sid from [{user_id}]
        rect rgba(160, 160, 160, 0.5)
        B->>A: emit teacher_force_logout {"user_id": ""}
        end




    ```
