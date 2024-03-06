# on_disconnect

- #### Infra

  - [x] Redis
  - [ ] RDS

- #### Client

  - [x] Teacher App
  - [x] Participant
  - [x] Hub

- #### Server Event Handler

  - data

    ```
    None
    ```

  - callback
    ```
    None
    ```

- #### Client Event Handler

  - listener: Hub
  - event name: teacher_disconnect
  - channel: org_id
  - data:
    ```
      {
        "user_id": str
      }
    ```

- ## Flow

  - ### 1. Teacher APP Disconnect

    ```mermaid
    sequenceDiagram
      autonumber
        participant A as Teacher APP
        participant B as Socket Server
        participant R as Redis
        participant H as Hub


        A->>B: emit disconnect
        B->>B: get session {"role":str,"client_id":str,"lesson_id":str,"org_id":str,"product_type":str"}
        R->>B: set {state:disconnect} to [alive:org_{org_id}_user_{user_id}] & TTL 1 hr.
        rect rgba(160, 160, 160, 0.5)
        B->>H: emit "teacher_disconnect"  {"user_id": client_id}
        end
        B->>B: leave_room(sid,lesson_id)


    ```

  - ### 2. Hub Disconnect

    ```mermaid
    sequenceDiagram
    autonumber
        participant A as Hub
        participant B as Socket Server
        A->>B: emit disconnect
        B->>B: get session {"role":str,"client_id":str,"lesson_id":str,"org_id":str,"product_type":str"}
        B->>B: leave_room(sid,lesson_id)

    ```

  - ### 3. Participant Disconnect

    ```mermaid
    sequenceDiagram
       autonumber
        participant A as Participant
        participant B as Backend
        participant R as Redis
        A->>B: emit disconnect
        B->>B: get session {"role":str,"client_id":str,"lesson_id":str,"org_id":str,"product_type":str"}
        alt [if lesson exist]
        B->>R: get room_id from [lesson_room_{lesson_id}]
        B->>B: call mixpanel disconnect
        B->>B: leave_room(sid,lesson_id)
        end

    ```
