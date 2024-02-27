- # 事件名稱: connect

- ## Request(queryString):

  ```
  role=teacher/student
  org_id='{org_id}'
  product_type= manager (optional)(TeacherHub need)
  auth=access_token
  ```

- Example request:

  - TeacherApp:
    ```
    role=teacher
    org_id={org_id}
    auth=access_token
    ```
  - ParticipantWeb:
    ```
    role=student
    ```
  - TeacherHub:
    ```
    role=teacher/admin
    org_id={org_id}
    product_type= manager
    auth=access_token
    ```

- ## CallBackResponse:

      None

- ## Relative Infrastructure

  1. Redis

- ## Usecase

  - ### 1. TeacherAPP Connect

    - #### Clients:

      1. TeacherAPP: TeacherAPP 上線

    - #### Listeners:

      1. TeacherHub：APP 會接收到此使用者上線的通知。

    - #### Response(Listeners):

      1. TeacherHub:

         - event_name = 'teacher_login'
           ```
             {"user_id": client_id, "display_name": display_name}
           ```
         - broadcast_channel:

           ```
              org_id
           ```

      - #### FLOW

        ```mermaid
        sequenceDiagram

                participant A as TeacherAPP
                participant B as Backend
                participant R as Redis
                participant M as TeacherHub

                A->>B: connect
                B->>R: add "alive:org_{org_id}_user_{user_id}" key {login_time:int,state:connect}
                R->>B:success
                B->>R: set "user_id" key {"sid":sid,client_id": user_id,"role": role,"org_id": org_id}
                R->>B:success
                B->>M: emit "teacher_login" to TeacherHub  {"user_id": client_id, "display_name": display_name}
                alt reconnected for mixpanel
                    alt get_lesson_id
                        B->>B:call mixpanel reconnect
                        %% B->>R:check "lesson_room_{lesson_id}" key exists
                        %%alt if not "lesson_room_{lesson_id}" key exists
                            %%B->>DB: query DB
                            %%DB->>B: room_id
                            %%B->>R: set lesson_room_{lesson_id}" key
                        %%end

                        %%B->>B:call mixpanel reconnect
                    end

                end

        ```

  - ### 2. TeacherHub Connect

    - #### Clients:

      1. TeacherHub : TeacherHub 上線

    - #### Listeners:

          None

    - #### Response(Listeners):

          None

    - #### FLOW

      ```mermaid
      sequenceDiagram

          participant A as TeacherHub
          participant B as Backend
          participant R as Redis
          A->>B: connect
          B->>R: enter_room(room_id=org_id)
          alt reconnected
              alt get_lesson_id
                  B->>B:call mixpanel reconnect
              end

          end

      ```

  - ### 3. ParticipantWeb Connect

    - #### Clients:

      1.  ParticipantWeb : ParticipantWeb 上線

    - #### Listeners:

          None

    - #### Response(Listeners):

          None

      - #### FLOW

        ```mermaid
        sequenceDiagram

            participant A as ParticipantWeb
            participant B as Backend
            participant R as Redis
            A->>B: connected
            B->>R: set "user_id" key {"sid":sid,"client_id": user_id,"role": role,"org_id": org_id}
            R->>B:success
            alt reconnected

                alt get_lesson_id
                    B->>B:call mixpanel reconnect
                end

            end
        ```
