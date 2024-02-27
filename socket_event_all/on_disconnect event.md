- # 事件名稱: disconnect

- ## Request(client emit data):

      None

- ## CallBackResponse:

      None

- ## Relative Infrastructure

  1. Redis

- ## Usecase

  - ### 1. TeacherAPP Disconnect

    - #### Clients:

      1. TeacherAPP: TeacherAPP 斷線

    - #### Listeners:

      1. TeacherHub：接收到此 TeacherAPP 使用者斷線的通知。

    - #### Response(Listeners):

      1. TeacherHub:

         - event_name = 'teacher_disconnect'
           ```
             {"user_id": client_id}
           ```
         - broadcast_channel:

           ```
              org_id
           ```

      - #### FLOW

        ```mermaid
        sequenceDiagram

            participant A as client
            participant B as BackendSocket
            participant R as Redis
            participant H as TeacherHub


            A->>B: 1. disconnected

            B->>R: 2. update "alive:org_{org_id}_user_{user_id}" key {state:disconnect} & TTL 1 hr.
            R->>B: success
            B->>H: 3. emit "teacher_disconnect"  {"user_id": client_id}
            B->>B: 4. leave_room(sid,lesson_id)


        ```

  - ### 2. TeacherHub Disconnect

    - #### Clients:

      1. TeacherHub: TeacherHub 斷線

    - #### Listeners:

          None

    - #### Response(Listeners):

          None

    - #### FLOW

      ```mermaid
      sequenceDiagram

          participant A as TeacherHub
          participant B as Backend
          A->>B: 1. disconnect
          B->>B: 2. leave_room(sid,lesson_id)

      ```

  - ### 3. ParticipantWeb Connect

    - #### Clients:

      1. ParticipantWeb: ParticipantWeb 斷線

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
          A->>B: 1. disconnect
          B->>R: 2. get room_id in Redis
          R->>B:success
          B->>B: 3. call mixpanel disconnect
          B->>B: 4.leave_room(sid,lesson_id)

      ```
