{
  "steps": [
    {
      "function": "get_greeting",
      "module": "main_library.get_greeting",
      "endpoint": "/greeting",
      "methods": [
        "POST"
      ],
      "parameters": []
    },
    {
      "function": "create_servicenow_incident",
      "module": "main_library.create_servicenow_incidenet",
      "endpoint": "/create_servicenow_incident",
      "methods": [
        "POST"
      ],
      "parameters": [
        {
          "name": "description",
          "type": "body"
        }
      ]
    },
    {
      "function": "view_ticket_detailed",
      "module": "main_library.view_servicenow_incident",
      "endpoint": "/view_servicenow_incident",
      "methods": [
        "GET"
      ],
      "parameters": [
        {
          "name": "incident_id",
          "type": "body"
        },
        {
          "name": "sys_id",
          "type": "body"
        }
      ]
    },
    {
      "function": "get_auth_url_microsoft",
      "module": "main_library.microsoft_auth_graph_api",
      "endpoint": "/microsoft/login",
      "methods": [
        "GET"
      ],
      "parameters": [],
      "response_type": "redirect"
    },
    {
      "function": "handle_callback",
      "module": "main_library.microsoft_auth_graph_api",
      "endpoint": "/getAToken",
      "methods": [
        "GET"
      ],
      "parameters": [
        {
          "name": "code",
          "type": "query"
        },
        {
          "name": "error",
          "type": "query"
        },
        {
          "name": "error_description",
          "type": "query"
        }
      ]
    },
    {
      "function": "semantic_search_and_answer",
      "module": "main_library.Milvus_VectorDB_extraction",
      "endpoint": "/fetch_data_from_milvus",
      "methods": [
        "POST"
      ],
      "parameters": [
        {
          "name": "question",
          "type": "body"
        }
      ]
    }
  ]
}