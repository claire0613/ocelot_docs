- # 事件名稱: teacher_logout

- ## Request(client emit data):

       {
          user_id:"",
          org_id:"",
       }

- ## CallBackResponse:

      None

- ## Relative Infrastructure

  1. Redis

- ## Usecase

  - ### 1. TeacherAPP logout

    - #### Clients:

      1. TeacherAPP: 登出。

    - #### Listeners:

      1. TeacherHub：TeacherHub 會接收到 TeacherAPP 登出的通知。

    - #### Response(Listeners):

      1. TeacherHub:

         - event_name = 'teacher_logout'
           ```
             {"user_id": {user_id}}
           ```
         - broadcast_channel:

           ```
              org_id
           ```

    - #### FLOW

    ```mermaid
    sequenceDiagram
        autonumber
        participant A as TeacherAPP
        participant B as Backend
        participant R as Redis
        participant H as TeacherHub


        A->>B: 1. teacher_logout
        B->>R: 2. remove "alive:org_{org_id}_user_{user_id}" key
        R->>B: success
        B->>H: 3. emit all TeacherHub in same org  {"user_id":{user_id}}

    ```
