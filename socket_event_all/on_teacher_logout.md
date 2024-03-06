# on_teacher_logout

- #### Infra

  - [x] Redis
  - [ ] RDS

- #### Client

  - [x] Teacher App
  - [ ] Participant
  - [ ] Hub

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

  - listener: Hub
  - event name: teacher_logout
  - channel: org_id
  - data:
    ```
      {
        "user_id": str,
      }
    ```

- ## Flow

  - ### 1. Teacher APP

    ```mermaid
    sequenceDiagram
        autonumber
        participant A as Teacher APP
        participant B as Socket Server
        participant R as Redis
        participant H as Hub


        A->>B: emit teacher_logout(user_id,org_id)
        R->>B: delete ["alive:org_{org_id}_user_{user_id}"]
        rect rgba(160, 160, 160, 0.5)
        B->>H: emit teacher_logout {"user_id":{user_id}}
        end

    ```
