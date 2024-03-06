# on_join_lesson

- #### Infra

  - [x] Redis
  - [x] RDS

- #### Client

  - [x] Teacher App
  - [x] Participant
  - [ ] Hub

- #### Server Event Handler

  - data

    ```
    None
    ```

  - callback

    - SUCCESS

      ```
        {
            "status": "SUCCESS",
            "data": {}
        }
      ```

      - ERROR

        ```
        {
          "status": "ERROR",
          "message": str(e)
        }
        ```

- #### Client Event Handler

  ```
    None
  ```

- ## Flow

  - ### 1. Teacher APP

    ```mermaid
        sequenceDiagram
            autonumber
            participant A as Teacher APP
            participant B as Socket Server
            participant R as Redis
            participant D as RDS

            A->>B: emit join_lesson
            B->>D: check_lesson_exists
            alt if not lesson exists
              D->>B: not found lesson_id
              B->>A: return error
            end
            B->>B: enter_room
            D->>B : get seat
            B->>B : get session
            alt if seat
                B->>B: add {'seat':seat} in session
            end
            B->>B: save session
            R->>B: get lesson_seat_in_redis from [lesson_seat_{lesson_id}]
            alt if not lesson_seat_* exists
                R->>B: set  {1:"",2:""....} to [lesson_seat_{lesson_id}]
            end
            R->>B: set {{user_id}:sid} to [lesson_teacher_{lesson_id}] & TTL 24hrs
            R->>B: set {"lesson_id": lesson_id} to [{user_id}]
            B->>A: return success

    ```

  - ### 2. Participant

    ```mermaid
    sequenceDiagram

        participant A as Participant
        participant B as Socket Server
        participant R as Redis
        participant D as RDS

        A->>B: emit join_lesson
        B->>D: check_lesson_exists
        alt if not lesson exists
          D->>B: not found lesson_id
          B->>A: return error
        end
        B->>B: enter_room
        D->>B : get seat
        B->>B : get session
        alt if seat
            B->>B: add {'seat':seat} in session
        end
        B->>B: save session
        R->>B: get lesson_seat_in_redis from [lesson_seat_{lesson_id}]
        alt if not lesson_seat_* exists
            R->>B: set  {1:"",2:""....} to [lesson_seat_{lesson_id}]
        end
        alt if access_token is not None
            B->>B: get client_id by access_token
            B->>B: save session {"client_id":str,"role":str}
            R->>B:  get {client_id} key exists
            alt if {client_id} key exists
                B->>B: call mixpanel reconnect
            end
          R->>B: set {"sid":str,"client_id":str,"role":str} to [{client_id}] & TTL 24 hr
          R->>B: set {"{client_id}":sid} to [lesson_student_{lesson_id}]
        end
        B->>A: return success

    ```
