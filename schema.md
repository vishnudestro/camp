# Sign up(Admin)
```JSON
"dta":{

}
```

```JSON
"admin_user":[
    {
        "email":"xxxx@gmail.com",
        "company_name": "xxxx",
        "job_title": "COO",
        "password": "..........",
        "team_selection":[], #it is optional if not filled by user it will be null.
        "any_projects":[], #it is optional if not filled by user it will be null.
        "co_worker": 
        {
            "email": "xxxx@gmail.com", 
            "name": "xxxx"
        } #it is optional if not filled by user it will be null.

    }
]
```

# Sign up (User)
```JSON
"user":[
    {
        "name": "xxxx",
        "email": "xxx@gmail.com",
        "password": "..........",
        "tile": "xxxx"
    }
]
```

# organization

```JSON
"organization":[
    {

        "org_name":"PNA",
        "org_id":1234567,
        "people_id":[1,2,3,4,5],
        "team_id":[1,2]
    
    }
]
```

# User profile

```JSON
"users":[
    {
        "user_name":,
        "user_id":,
        "email":,
        "password":,
        "role":,
        "team_id":[3, 4],
        "project_id":[12, 23]
    }
]
```

# Message board

```JSON
"message":[
    {
        "message_id":123,
        "title":"sample",
        "message":"A sample message",
        "author_id":3,
        "date": "date",
        "time": "time",
        "people_to_notify":[1,2,3,4]
    }
]
```

# Team

```JSON
"team":[
    {
        "team_name":"Development",
        "team_id":123,
        "people_id":[3,5,6]
    }
]
```

# Projects

```JSON
"projects":[
    {
        "project_name":"Sample",
        "project_id":345,
        "people_id":[7,4,3]

    }
]
```

# To create a To-do
```JSON
{   
    "team_id": "team_id (or) None",
    "project_id":"project_id (or) None",
    "title" : "xxxx"
}
```

# To-do list

```JSON
"to_do":[
    {
        "task_name": "sample",
        "task_id": "123",
        "to_do_list":[
            {
                "to_do_id":345,
                "title": "sample",
                "assigned_to(people_id)": [3,4,5],
                "notify_to(people_id)": [2],
                "starts_on": "date",
                "due_deleiver_date": "date",
                "deleivered_at": "date",
                "mark_as_done": "True or False",
                "overdue":"True or False",
                "comments" :[
                    {
                        "person_name":"comments"
                    }
                ]
            }
        ]

    }
]
```

# Automatic Check In's

```JSON
"check_ins":[
    {
        "check_in_id":45,
        "question": "what do you work on today",
        "days":["monday","Tuesday"],
        "period_of_asking":
        {
            "daily":"True (or) False",
            "once_a_week":"True (or) False",
            "every_other_week":"True (or) False",
            "once_a_month":"True (or) False"
        },
        "asking_time":"time",
        "person_to_ask(people_id)":[3,4,5]
    }
]
```
# sample 

```JSON
"user_id":[
    {
        "company_name":
        {
            "to_do":[
                {
                    "todo_name":"xxx",
                    "todo_id":1234,
                    "created_at": "date",
                    "Done_at":"date",
                    "to_do":[
                        {
                            "to_do_id":345,
                            "title": "sample",
                            "assigned_to(people_id)": [3,4,5],
                            "notify_to(people_id)": [2],
                            "created_at": "date",
                            "actual_deleiver_date": "date",
                            "deleivered_at": "date"
                        }
                    ]    
                },
                {
                    "todo_name":"xxx",
                    "todo_id":1234,
                    "created_at": "date",
                    "Done_at":"date",
                    "to_do":[
                        {
                            "to_do_id":345,
                            "title": "sample",
                            "assigned_to(people_id)": [3,4,5],
                            "notify_to(people_id)": [2],
                            "created_at": "date",
                            "actual_deleiver_date": "date",
                            "deleivered_at": "date"
                        }
                    ]
                }
            ]
        },
        
        "team":
        {
            "team_name":
            {
                "to_do":[
                    {
                        "todo_name":"xxx",
                        "todo_id":1234,
                        "created_at": "date",
                        "Done_at":"date",
                        "to_do":[
                            {
                                "to_do_id":345,
                                "title":"sample",
                                "assigned_to(people_id)": [3,4,5],
                                "notify_to(people_id)": [2],
                                "created_at": "date",
                                "actual_deleiver_date": "date",
                                "deleivered_at": "date"

                            }
                        ]
                    },
                    {
                        "todo_name":"xxx",
                        "todo_id":1234,
                        "created_at": "date",
                        "Done_at":"date",
                        "to_do":[
                            {
                                "to_do_id":345,
                                "title":"sample",
                                "assigned_to(people_id)": [3,4,5],
                                "notify_to(people_id)": [2],
                                "created_at": "date",
                                "actual_deleiver_date": "date",
                                "deleivered_at": "date"

                            }
                        ]
                    }
                ]
            }
        },
        
        "projects":
        {
            "to_do":[
                {
                        "todo_name":"xxx",
                        "todo_id":1234,
                        "created_at": "date",
                        "Done_at":"date",
                        "to_do":[
                            {
                                "to_do_id":345,
                                "title":"sample",
                                "assigned_to(people_id)": [3,4,5],
                                "notify_to(people_id)": [2],
                                "created_at": "date",
                                "actual_deleiver_date": "date",
                                "deleivered_at": "date"

                            }
                        ]
                    },
                    {
                        "todo_name":"xxx",
                        "todo_id":1234,
                        "created_at": "date",
                        "Done_at":"date",
                        "to_do":[
                            {
                                "to_do_id":345,
                                "title":"sample",
                                "assigned_to(people_id)": [3,4,5],
                                "notify_to(people_id)": [2],
                                "created_at": "date",
                                "actual_deleiver_date": "date",
                                "deleivered_at": "date"

                            }
                        ]
                    }
            ]
        }
    }
]
```

# Dashboard

```JSON
"hq":{   
        "hq":"company_name",
        "hq_id": "company_id",
        "description":"<some message>"
    },
    "divisions":{
        "team":[
            {
                "team_name": "xxxx",
                "team_id": 1234,
                "description":"<some message>"
            },
            {
                "team_name": "yyyy",
                "team_id": 5678,
                "description":"<some message>"
            },
            {
                "team_name": "zzzz",
                "team_id": 9087,
                "description":"<some message>"
            }
        ],
        "projects":[
            {
                "project_name": "xxxx",
                "project_id": 1234,
                "description":"<some message>"
            },
            {
                "project_name": "xxxx",
                "project_id": 5678,
                "description":"<some message>"
            },
            {
                "project_name": "xxxx",
                "project_id": 9087,
                "description":"<some message>"
            }
        ]
    }
]
```

