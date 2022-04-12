UPDATE_TAGS_RESPONSE = [
    {
        "tagId": 1,
        "entity": "experiment",
        "entityId": 3,
        "dtCreated": "2020-02-01T12:46:58.506Z",
        "dtDeleted": None,
        "userId": 1,
        "id": 1,
        "entity_id": 3,
        "tag": {
            "name": "test0",
            "dtCreated": "2020-02-01T12:46:58.480Z",
            "id": 1
        }
    },
    {
        "tagId": 2,
        "entity": "experiment",
        "entityId": 3,
        "dtCreated": "2020-02-01T12:46:58.507Z",
        "dtDeleted": None,
        "userId": 1,
        "id": 2,
        "entity_id": 3,
        "tag": {
            "name": "test2",
            "dtCreated": "2020-02-01T12:46:58.481Z",
            "id": 2
        }
    },
    {
        "tagId": 3,
        "entity": "experiment",
        "entityId": 3,
        "dtCreated": "2020-02-01T12:46:58.509Z",
        "dtDeleted": None,
        "userId": 1,
        "id": 3,
        "entity_id": 3,
        "tag": {
            "name": "test1",
            "dtCreated": "2020-02-01T12:46:58.482Z",
            "id": 3
        }
    },
    {
        "tagId": 4,
        "entity": "experiment",
        "entityId": 3,
        "dtCreated": "2020-02-01T12:46:58.510Z",
        "dtDeleted": None,
        "userId": 1,
        "id": 4,
        "entity_id": 3,
        "tag": {
            "name": "test3",
            "dtCreated": "2020-02-01T12:46:58.483Z",
            "id": 4
        }
    }
]

GET_TAGS_RESPONSE = {
    "some_id": [
        {
            "tagId": 1,
            "entity": "entity",
            "entityId": 3,
            "dtCreated": "2020-02-01T12:46:58.506Z",
            "dtDeleted": None,
            "userId": 1,
            "id": 1,
            "entity_id": 3,
            "tag": {
                "name": "test0",
                "dtCreated": "2020-02-01T12:46:58.480Z",
                "id": 1
            }
        },
        {
            "tagId": 2,
            "entity": "entity",
            "entityId": 3,
            "dtCreated": "2020-02-01T12:46:58.507Z",
            "dtDeleted": None,
            "userId": 1,
            "id": 2,
            "entity_id": 3,
            "tag": {
                "name": "test2",
                "dtCreated": "2020-02-01T12:46:58.481Z",
                "id": 2
            }
        },
        {
            "tagId": 3,
            "entity": "entity",
            "entityId": 3,
            "dtCreated": "2020-02-01T12:46:58.509Z",
            "dtDeleted": None,
            "userId": 1,
            "id": 3,
            "entity_id": 3,
            "tag": {
                "name": "test1",
                "dtCreated": "2020-02-01T12:46:58.482Z",
                "id": 3
            }
        },
        {
            "tagId": 4,
            "entity": "entity",
            "entityId": 3,
            "dtCreated": "2020-02-01T12:46:58.510Z",
            "dtDeleted": None,
            "userId": 1,
            "id": 4,
            "entity_id": 3,
            "tag": {
                "name": "test3",
                "dtCreated": "2020-02-01T12:46:58.483Z",
                "id": 4
            }
        }
    ]
}

CREATE_MACHINE_RESPONSE = {
    "id": "psclbvqpc",
    "name": "some_machine",
    "os": None,
    "ram": None,
    "cpus": 1,
    "gpu": None,
    "storageTotal": None,
    "storageUsed": None,
    "usageRate": "Pro hourly",
    "shutdownTimeoutInHours": 168,
    "shutdownTimeoutForces": False,
    "performAutoSnapshot": False,
    "autoSnapshotFrequency": None,
    "autoSnapshotSaveCount": None,
    "dynamicPublicIp": False,
    "agentType": "WindowsDesktop",
    "dtCreated": "2019-04-10T14:19:49.852Z",
    "state": "provisioning",
    "updatesPending": False,
    "networkId": None,
    "privateIpAddress": None,
    "publicIpAddress": None,
    "region": None,
    "userId": "u3z4be26",
    "teamId": "te6hh34n6",
    "scriptId": None,
    "dtLastRun": None
}

LIST_MACHINES_RESPONSE = [
    {
        "ram": None,
        "userId": "u3z4be26",
        "cpus": 1,
        "teamId": "te6hh34n6",
        "updatesPending": False,
        "dynamicPublicIp": False,
        "storageTotal": None,
        "shutdownTimeoutForces": False,
        "id": "psclbvqpc",
        "shutdownTimeoutInHours": 168,
        "state": "provisioning",
        "usageRate": "Pro hourly",
        "publicIpAddress": None,
        "gp": None,
        "privateIpAddress": None,
        "dtCreated": "2019-04-10T14:19:49.852Z",
        "dtLastRun": None,
        "storageUsed": None,
        "scriptId": None,
        "autoSnapshotSaveCount": None,
        "name": "keton2",
        "agentType": "WindowsDesktop",
        "performAutoSnapshot": False,
        "networkId": None,
        "autoSnapshotFrequency": None,
        "os": None, "region": None
    },
    {
        "ram": "536870912",
        "userId": "u3z4be26",
        "cpus": 1,
        "teamId": "te6hh34n6",
        "updatesPending": False,
        "dynamicPublicIp": False,
        "storageTotal": "53687091200",
        "shutdownTimeoutForces": False,
        "id": "psbtuwfvt",
        "shutdownTimeoutInHours": 1,
        "state": "off",
        "usageRate": "C1 Hourly",
        "publicIpAddress": None,
        "gp": "None",
        "privateIpAddress": "10.64.14.135",
        "dtCreated": "2019-04-11T18:10:29.665Z",
        "dtLastRun": None,
        "storageUsed": "110080",
        "scriptId": None,
        "autoSnapshotSaveCount": 1,
        "name": "New Machine 1",
        "agentType": "LinuxHeadless",
        "performAutoSnapshot": True,
        "networkId": "nng82wb",
        "autoSnapshotFrequency": "month",
        "os": "Ubuntu 18.04.1 LTS; uname: 4.15.0-38-generic; distro: ubuntu; major: 18; minor: 04",
        "region": "East Coast (NY2)"
    }
]

SHOW_MACHINE_RESPONSE = {
    "id": "some_id",
    "name": "New Machine 1",
    "os": "Ubuntu 18.04.1 LTS; uname: 4.15.0-38-generic; distro: ubuntu; major: 18; minor: 04",
    "ram": "536870912",
    "cpus": 1,
    "gpu": "None",
    "storageTotal": "53687091200",
    "storageUsed": "110080",
    "usageRate": "C1 Hourly",
    "shutdownTimeoutInHours": 1,
    "shutdownTimeoutForces": False,
    "performAutoSnapshot": True,
    "autoSnapshotFrequency": "month",
    "autoSnapshotSaveCount": 1,
    "dynamicPublicIp": False,
    "agentType": "LinuxHeadless",
    "dtCreated": "2019-04-11T18:10:29.665Z",
    "state": "off",
    "updatesPending": False,
    "networkId": "nng82wb",
    "privateIpAddress": "10.64.14.135",
    "publicIpAddress": None,
    "region": "East Coast (NY2)",
    "userId": "u3z4be26",
    "teamId": "te6hh34n6",
    "scriptId": None,
    "dtLastRun": None,
    "events": [
        {
            "name": "restart",
            "state": "done",
            "errorMsg": "",
            "handle": "042454c4-af4c-489a-8bff-b4d3e9f39f9e",
            "dtModified": "2019-04-12T12:19:05.801Z",
            "dtFinished": "2019-04-12T12:19:05.801Z",
            "dtCreated": "2019-04-12T12:19:03.814Z"
        },
        {
            "name": "stop",
            "state": "done",
            "errorMsg": "",
            "handle": "07fe20ce-35c4-4949-afbd-103d1afc6797",
            "dtModified": "2019-04-11T19:11:19.942Z",
            "dtFinished": "2019-04-11T19:11:19.942Z",
            "dtCreated": "2019-04-11T19:11:14.205Z"
        },
        {
            "name": "snapshot-create",
            "state": "done",
            "errorMsg": "",
            "handle": "7fa0ab4f-896d-42ac-a2c5-54f0a94c2310",
            "dtModified": "2019-04-11T18:14:36.702Z",
            "dtFinished": "2019-04-11T18:14:36.702Z",
            "dtCreated": "2019-04-11T18:14:33.216Z"
        },
        {
            "name": "start",
            "state": "done",
            "errorMsg": "",
            "handle": "c04cccdf-3823-4ef1-b1ab-83b3ccdcfcb7",
            "dtModified": "2019-04-11T18:11:00.371Z",
            "dtFinished": "2019-04-11T18:11:00.371Z",
            "dtCreated": "2019-04-11T18:10:45.468Z"
        },
        {
            "name": "create",
            "state": "done",
            "errorMsg": "",
            "handle": "34f64d24-1161-42f0-871d-1ed03b10dfc0",
            "dtModified": "2019-04-11T18:10:45.473Z",
            "dtFinished": "2019-04-11T18:10:45.473Z",
            "dtCreated": "2019-04-11T18:10:29.665Z"
        }
    ]
}

SHOW_MACHINE_UTILIZATION_RESPONSE = {
    "machineId": "some_key",
    "utilization": {
        "machineId": "some_key",
        "secondsUsed": 0,
        "billingMonth": "2017-09",
        "hourlyRate": 0,
    },
    "storageUtilization": {
        "machineId": "some_key",
        "secondsUsed": 256798.902394,
        "monthlyRate": "5.00",
        "billingMonth": "2017-09",
    },
}

LIST_PROJECTS_RESPONSE = {
    "data": [
        {
            "name": "test_project",
            "handle": "prq70zy79",
            "dtCreated": "2019-03-18T13:24:46.666Z",
            "dtDeleted": None,
            "lastJobSeqNum": 2,
            "repoNodeId": None,
            "repoName": None,
            "repoUrl": None,
        },
        {
            "name": "keton",
            "handle": "prmr22ve0",
            "dtCreated": "2019-03-25T14:50:43.202Z",
            "dtDeleted": None,
            "lastJobSeqNum": 8,
            "repoNodeId": None,
            "repoName": None,
            "repoUrl": None,
        },
        {
            "name": "paperspace-python",
            "handle": "przhbct98",
            "dtCreated": "2019-04-04T15:12:34.229Z",
            "dtDeleted": None,
            "lastJobSeqNum": 3,
            "repoNodeId": None,
            "repoName": None,
            "repoUrl": None,
        }
    ],
    "meta": {
        "totalItems": 3
    }
}

LIST_MODELS_RESPONSE_JSON = {
    "modelList": [
        {
            "id": "mosu30xm7q8vb0p",
            "projectId": "prmr22ve0",
            "modelType": "Tensorflow",
            "name": None,
            "tag": None,
            "summary": {
                "loss": {
                    "result": {
                        "max": 0.028335485607385635,
                        "min": 0.028335485607385635,
                        "var": 0,
                        "mean": 0.028335485607385635,
                        "median": 0.028335485607385635,
                        "stddev": 0
                    },
                    "scalar": "loss"
                },
                "accuracy": {
                    "result": {
                        "max": 0.991100013256073,
                        "min": 0.991100013256073,
                        "var": 0,
                        "mean": 0.991100013256073,
                        "median": 0.991100013256073,
                        "stddev": 0
                    },
                    "scalar": "accuracy"
                }
            },
            "detail": [
                {
                    "scalars": [
                        {
                            "data": [
                                {
                                    "operation": "mean",
                                    "checkpoints": [
                                        {
                                            "value": 0.0621405728161335,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.039062466472387314,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.03250512480735779,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.025037841871380806,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.02336057461798191,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.024296583607792854,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.021974526345729828,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.021116264164447784,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.020851025357842445,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.022611157968640327,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.028335485607385635,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "amin",
                                    "checkpoints": [
                                        {
                                            "value": 0.0621405728161335,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.039062466472387314,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.03250512480735779,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.025037841871380806,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.02336057461798191,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.024296583607792854,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.021974526345729828,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.021116264164447784,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.020851025357842445,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.022611157968640327,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.028335485607385635,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "amax",
                                    "checkpoints": [
                                        {
                                            "value": 0.0621405728161335,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.039062466472387314,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.03250512480735779,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.025037841871380806,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.02336057461798191,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.024296583607792854,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.021974526345729828,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.021116264164447784,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.020851025357842445,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.022611157968640327,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.028335485607385635,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "median",
                                    "checkpoints": [
                                        {
                                            "value": 0.0621405728161335,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.039062466472387314,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.03250512480735779,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.025037841871380806,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.02336057461798191,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.024296583607792854,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.021974526345729828,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.021116264164447784,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.020851025357842445,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.022611157968640327,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.028335485607385635,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "std",
                                    "checkpoints": [
                                        {
                                            "value": 0,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "var",
                                    "checkpoints": [
                                        {
                                            "value": 0,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 12000
                                        }
                                    ]
                                }
                            ],
                            "scalar": "loss"
                        },
                        {
                            "data": [
                                {
                                    "operation": "mean",
                                    "checkpoints": [
                                        {
                                            "value": 0.9804999828338623,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.9872000217437744,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.9904000163078308,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.9912999868392944,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.9919999837875366,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.991599977016449,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.992900013923645,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.9922000169754028,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.9930999875068665,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.9926000237464905,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.991100013256073,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "amin",
                                    "checkpoints": [
                                        {
                                            "value": 0.9804999828338623,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.9872000217437744,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.9904000163078308,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.9912999868392944,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.9919999837875366,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.991599977016449,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.992900013923645,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.9922000169754028,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.9930999875068665,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.9926000237464905,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.991100013256073,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "amax",
                                    "checkpoints": [
                                        {
                                            "value": 0.9804999828338623,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.9872000217437744,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.9904000163078308,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.9912999868392944,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.9919999837875366,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.991599977016449,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.992900013923645,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.9922000169754028,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.9930999875068665,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.9926000237464905,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.991100013256073,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "median",
                                    "checkpoints": [
                                        {
                                            "value": 0.9804999828338623,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0.9872000217437744,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0.9904000163078308,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0.9912999868392944,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0.9919999837875366,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0.991599977016449,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0.992900013923645,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0.9922000169754028,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0.9930999875068665,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0.9926000237464905,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0.991100013256073,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "std",
                                    "checkpoints": [
                                        {
                                            "value": 0,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 12000
                                        }
                                    ]
                                },
                                {
                                    "operation": "var",
                                    "checkpoints": [
                                        {
                                            "value": 0,
                                            "checkpoint": 1175
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 2323
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 3471
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 4606
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 5785
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 6956
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 8116
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 9262
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 10397
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 11566
                                        },
                                        {
                                            "value": 0,
                                            "checkpoint": 12000
                                        }
                                    ]
                                }
                            ],
                            "scalar": "accuracy"
                        }
                    ],
                    "session": "eval"
                }
            ],
            "params": None,
            "url": "s3://ps-projects-development/prmr22ve0/ehla1kvbwzaco/model/",
            "notes": None,
            "isDeleted": False,
            "isPublic": False,
            "dtCreated": "2019-04-02T17:02:47.157Z",
            "dtModified": "2019-04-02T17:02:54.273Z",
            "dtUploaded": "2019-04-02T17:02:54.273Z",
            "dtDeleted": None,
            "modelPath": "/artifacts"
        }
    ],
    "total": 1,
    "displayTotal": 1
}

NOTEBOOK_GET_RESPONSE = {
    "name": "some_name",
    "handle": "ngw7piq9",
    "jobHandle": "jzhmk7fpluqje",
    "project": "Notebook-some_name",
    "projectHandle": "prg284tu2",
    "state": "Running",
    "token": "dc2c331ce694ebe5a615f6e5885f6a933fcb1be49cb0d17f",
    "container": "Paperspace + Fast.AI 1.0 (V3)",
    "containerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
    "baseContainer": "Paperspace + Fast.AI 1.0 (V3)",
    "baseContainerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
    "vmType": "K80",
    "cluster": "PS Notebooks on GCP",
    "clusterId": "clmtkpnm2",
    "fqdn": "ngw7piq9.dgradient.paperspace.com",
    "startedByUser": "first last",
    "startedByUserId": "ukgvw4i8",
    "namespace": "some_namespace",
    "parentJobId": None,
    "jobError": None,
    "dtCreated": "2019-09-03T11:06:18.154Z",
    "dtModified": "2019-09-03T11:06:18.154Z",
    "dtProvisioningStarted": "2019-09-03T11:08:36.286Z",
    "dtProvisioningFinished": "2019-09-03T11:10:36.471Z",
    "dtStarted": "2019-09-03T11:10:36.471Z",
    "dtFinished": None,
    "dtTeardownStarted": None,
    "dtTeardownFinished": None,
    "dtDeleted": None,
    "shutdownTimeout": 6,
    "jobId": 20206,
    "isPublic": False,
    "isPreemptible": False,
    "cpuHostname": "gradient-host-1567508793",
    "cpuCount": 2,
    "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
    "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
    "cpuMem": "12297212 kB",
    "gpuName": "Tesla K80",
    "gpuSerial": "0320617088427",
    "gpuDevice": "/dev/nvidia0",
    "gpuDriver": "418.67",
    "gpuCount": 1,
    "gpuMem": "11441 MiB",
    "tpuType": None,
    "tpuName": None,
    "tpuGrpcUrl": None,
    "tpuTFVersion": None,
    "tpuDatasetDir": None,
    "tpuModelDir": None,
    "id": 1823,
    "metricsURL": "aws-testing.paperspace.io",
}

NOTEBOOK_GET_RESPONSE_WITH_TAGS = {
    "name": "some_name",
    "handle": "ngw7piq9",
    "jobHandle": "jzhmk7fpluqje",
    "project": "Notebook-some_name",
    "projectHandle": "prg284tu2",
    "state": "Running",
    "token": "dc2c331ce694ebe5a615f6e5885f6a933fcb1be49cb0d17f",
    "container": "Paperspace + Fast.AI 1.0 (V3)",
    "containerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
    "baseContainer": "Paperspace + Fast.AI 1.0 (V3)",
    "baseContainerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
    "vmType": "K80",
    "cluster": "PS Notebooks on GCP",
    "clusterId": "clmtkpnm2",
    "fqdn": "ngw7piq9.dgradient.paperspace.com",
    "startedByUser": "first last",
    "startedByUserId": "ukgvw4i8",
    "namespace": "some_namespace",
    "parentJobId": None,
    "jobError": None,
    "dtCreated": "2019-09-03T11:06:18.154Z",
    "dtModified": "2019-09-03T11:06:18.154Z",
    "dtProvisioningStarted": "2019-09-03T11:08:36.286Z",
    "dtProvisioningFinished": "2019-09-03T11:10:36.471Z",
    "dtStarted": "2019-09-03T11:10:36.471Z",
    "dtFinished": None,
    "dtTeardownStarted": None,
    "dtTeardownFinished": None,
    "dtDeleted": None,
    "shutdownTimeout": 6,
    "jobId": 20206,
    "isPublic": False,
    "isPreemptible": False,
    "cpuHostname": "gradient-host-1567508793",
    "cpuCount": 2,
    "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
    "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
    "cpuMem": "12297212 kB",
    "gpuName": "Tesla K80",
    "gpuSerial": "0320617088427",
    "gpuDevice": "/dev/nvidia0",
    "gpuDriver": "418.67",
    "gpuCount": 1,
    "gpuMem": "11441 MiB",
    "tpuType": None,
    "tpuName": None,
    "tpuGrpcUrl": None,
    "tpuTFVersion": None,
    "tpuDatasetDir": None,
    "tpuModelDir": None,
    "id": 1823,
    "tags": [
        "tag1",
        "tag2"
    ],
}

NOTEBOOKS_LIST_RESPONSE_JSON = {
    "notebookList": [
        {
            "name": "job 1",
            "handle": "n1vmfj6x",
            "jobHandle": "jsh0692p80dphg",
            "project": "Notebook-undefined",
            "projectHandle": "pr231zktg",
            "state": "Running",
            "token": "80426c989ef8d42b4dff6806c9592b1111a47c63c0f4a36f",
            "container": "Paperspace + Fast.AI 1.0 (V3)",
            "containerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
            "baseContainer": "Paperspace + Fast.AI 1.0 (V3)",
            "baseContainerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
            "vmType": "K80",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "n1vmfj6x.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": None,
            "dtCreated": "2019-09-04T11:06:12.667Z",
            "dtModified": "2019-09-04T11:06:12.667Z",
            "dtProvisioningStarted": "2019-09-04T11:08:28.305Z",
            "dtProvisioningFinished": "2019-09-04T11:10:30.628Z",
            "dtStarted": "2019-09-04T11:10:30.628Z",
            "dtFinished": None,
            "dtTeardownStarted": None,
            "dtTeardownFinished": None,
            "dtDeleted": None,
            "shutdownTimeout": None,
            "jobId": 20221,
            "isPublic": False,
            "isPreemptible": False,
            "cpuHostname": "gradient-host-1567595186",
            "cpuCount": 2,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "12297212 kB",
            "gpuName": "Tesla K80",
            "gpuSerial": "0320617028675",
            "gpuDevice": "/dev/nvidia0",
            "gpuDriver": "418.67",
            "gpuCount": 1,
            "gpuMem": "11441 MiB",
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1832
        },
        {
            "name": "job 1",
            "handle": "nhdf8zf3",
            "jobHandle": "jsyvcxoxch3jgu",
            "project": "Notebook-undefined",
            "projectHandle": "pr2u2sfja",
            "state": "Running",
            "token": "1d763ce770a195c98ea3d30588f3ad007c2b8403608ab091",
            "container": "Paperspace + Fast.AI 1.0 (V3)",
            "containerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
            "baseContainer": "Paperspace + Fast.AI 1.0 (V3)",
            "baseContainerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
            "vmType": "K80",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "nhdf8zf3.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": None,
            "dtCreated": "2019-09-04T10:23:04.762Z",
            "dtModified": "2019-09-04T10:23:04.762Z",
            "dtProvisioningStarted": "2019-09-04T10:26:05.190Z",
            "dtProvisioningFinished": "2019-09-04T10:28:13.609Z",
            "dtStarted": "2019-09-04T10:28:13.609Z",
            "dtFinished": None,
            "dtTeardownStarted": None,
            "dtTeardownFinished": None,
            "dtDeleted": None,
            "shutdownTimeout": None,
            "jobId": 20219,
            "isPublic": False,
            "isPreemptible": False,
            "cpuHostname": "gradient-host-1567592650-d5337953",
            "cpuCount": 2,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "12297204 kB",
            "gpuName": "Tesla K80",
            "gpuSerial": "0320617086962",
            "gpuDevice": "/dev/nvidia0",
            "gpuDriver": "418.67",
            "gpuCount": 1,
            "gpuMem": "11441 MiB",
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1831
        },
        {
            "name": "My Notebook 123",
            "handle": "nslk5r03",
            "jobHandle": "jskm7amsly7mmj",
            "project": "Notebook-My Notebook 123",
            "projectHandle": "pr3qq8qlg",
            "state": "Stopped",
            "token": "7751a516535bf3d52c164315d6187c1c9a04f15c15cf1c15",
            "container": "nslk5r03",
            "containerUrl": "us.gcr.io/ps-development-229517/paperspace/pr3qq8qlg:nslk5r03",
            "baseContainer": "Paperspace + Fast.AI 1.0 (V3)",
            "baseContainerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
            "vmType": "K80",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "nslk5r03.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": None,
            "dtCreated": "2019-09-04T10:22:43.248Z",
            "dtModified": "2019-09-04T10:22:43.248Z",
            "dtProvisioningStarted": "2019-09-04T10:25:26.545Z",
            "dtProvisioningFinished": "2019-09-04T10:27:24.319Z",
            "dtStarted": "2019-09-04T10:27:24.319Z",
            "dtFinished": "2019-09-04T16:27:52.044Z",
            "dtTeardownStarted": "2019-09-04T16:27:56.915Z",
            "dtTeardownFinished": "2019-09-04T16:28:57.796Z",
            "dtDeleted": None,
            "shutdownTimeout": 6,
            "jobId": 20218,
            "isPublic": False,
            "isPreemptible": False,
            "cpuHostname": "gradient-host-1567592577",
            "cpuCount": 2,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "12297212 kB",
            "gpuName": "Tesla K80",
            "gpuSerial": "0320617029024",
            "gpuDevice": "/dev/nvidia0",
            "gpuDriver": "418.67",
            "gpuCount": 1,
            "gpuMem": "11441 MiB",
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1830
        },
        {
            "name": "My Notebook 123",
            "handle": "ng9a3tp4",
            "jobHandle": "jg5vkj6d799z8",
            "project": "Notebook-My Notebook 123",
            "projectHandle": "pr5ngrxr9",
            "state": "Stopped",
            "token": "d9ba60e2bf7abd8ebd0c9988507ce203dd9baa7bc2b77284",
            "container": "ng9a3tp4",
            "containerUrl": "us.gcr.io/ps-development-229517/paperspace/pr5ngrxr9:ng9a3tp4",
            "baseContainer": "Paperspace + Fast.AI 1.0 (V3)",
            "baseContainerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
            "vmType": "K80",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "ng9a3tp4.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": None,
            "dtCreated": "2019-09-04T10:16:22.362Z",
            "dtModified": "2019-09-04T10:16:22.362Z",
            "dtProvisioningStarted": "2019-09-04T10:18:46.309Z",
            "dtProvisioningFinished": "2019-09-04T10:20:45.879Z",
            "dtStarted": "2019-09-04T10:20:45.879Z",
            "dtFinished": "2019-09-04T16:20:51.718Z",
            "dtTeardownStarted": "2019-09-04T16:20:56.745Z",
            "dtTeardownFinished": "2019-09-04T16:22:03.922Z",
            "dtDeleted": None,
            "shutdownTimeout": 6,
            "jobId": 20217,
            "isPublic": False,
            "isPreemptible": False,
            "cpuHostname": "gradient-host-1567592197",
            "cpuCount": 2,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "12297212 kB",
            "gpuName": "Tesla K80",
            "gpuSerial": "0320617086541",
            "gpuDevice": "/dev/nvidia0",
            "gpuDriver": "418.67",
            "gpuCount": 1,
            "gpuMem": "11441 MiB",
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1829
        },
        {
            "name": "some_name",
            "handle": "ngw7piq9",
            "jobHandle": "jzhmk7fpluqje",
            "project": "Notebook-some_name",
            "projectHandle": "prg284tu2",
            "state": "Stopped",
            "token": "dc2c331ce694ebe5a615f6e5885f6a933fcb1be49cb0d17f",
            "container": "ngw7piq9",
            "containerUrl": "us.gcr.io/ps-development-229517/paperspace/prg284tu2:ngw7piq9",
            "baseContainer": "Paperspace + Fast.AI 1.0 (V3)",
            "baseContainerUrl": "paperspace/fastai:1.0-CUDA9.2-base-3.0-v1.0.6",
            "vmType": "K80",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "ngw7piq9.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": None,
            "dtCreated": "2019-09-03T11:06:18.154Z",
            "dtModified": "2019-09-03T11:06:18.154Z",
            "dtProvisioningStarted": "2019-09-03T11:08:36.286Z",
            "dtProvisioningFinished": "2019-09-03T11:10:36.471Z",
            "dtStarted": "2019-09-03T11:10:36.471Z",
            "dtFinished": "2019-09-03T17:10:53.440Z",
            "dtTeardownStarted": "2019-09-03T17:10:54.455Z",
            "dtTeardownFinished": "2019-09-03T17:12:01.889Z",
            "dtDeleted": None,
            "shutdownTimeout": 6,
            "jobId": 20206,
            "isPublic": False,
            "isPreemptible": False,
            "cpuHostname": "gradient-host-1567508793",
            "cpuCount": 2,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "12297212 kB",
            "gpuName": "Tesla K80",
            "gpuSerial": "0320617088427",
            "gpuDevice": "/dev/nvidia0",
            "gpuDriver": "418.67",
            "gpuCount": 1,
            "gpuMem": "11441 MiB",
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1823
        },
        {
            "name": "some_notebook_name",
            "handle": "n8h0d5lf",
            "jobHandle": "js63sf787xc3mx",
            "project": "Notebook-some_notebook_name",
            "projectHandle": "prupasg3e",
            "state": "Error",
            "token": None,
            "container": "some_name",
            "containerUrl": "some_name",
            "baseContainer": "some_name",
            "baseContainerUrl": "some_name",
            "vmType": "G1",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "n8h0d5lf.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": "Error pulling container during provisioning for job js63sf787xc3mx: Error pulling image 'some_name': Error response from daemon: Get https://registry-1.docker.io/v2/library/some_name/manifests/latest: unauthorized: incorrect username or password",
            "dtCreated": "2019-08-30T12:31:43.392Z",
            "dtModified": "2019-08-30T12:31:43.392Z",
            "dtProvisioningStarted": "2019-08-30T12:33:34.650Z",
            "dtProvisioningFinished": None,
            "dtStarted": None,
            "dtFinished": "2019-08-30T12:33:35.479Z",
            "dtTeardownStarted": None,
            "dtTeardownFinished": None,
            "dtDeleted": None,
            "shutdownTimeout": 8,
            "jobId": 20163,
            "isPublic": False,
            "isPreemptible": True,
            "cpuHostname": "gradient-host-1567168315",
            "cpuCount": 1,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "1783380 kB",
            "gpuName": None,
            "gpuSerial": None,
            "gpuDevice": None,
            "gpuDriver": None,
            "gpuCount": None,
            "gpuMem": None,
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1811
        },
        {
            "name": "some_notebook_name",
            "handle": "nl0b6cn0",
            "jobHandle": "jss28gdrarcbrw",
            "project": "Notebook-some_notebook_name",
            "projectHandle": "pr43jj028",
            "state": "Error",
            "token": None,
            "container": "some_name",
            "containerUrl": "some_name",
            "baseContainer": "some_name",
            "baseContainerUrl": "some_name",
            "vmType": "G1",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "nl0b6cn0.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": "Error pulling container during provisioning for job jss28gdrarcbrw: Error pulling image 'some_name': Error response from daemon: Get https://registry-1.docker.io/v2/library/some_name/manifests/latest: unauthorized: incorrect username or password",
            "dtCreated": "2019-08-30T12:16:11.944Z",
            "dtModified": "2019-08-30T12:16:11.944Z",
            "dtProvisioningStarted": "2019-08-30T12:16:19.646Z",
            "dtProvisioningFinished": None,
            "dtStarted": None,
            "dtFinished": "2019-08-30T12:16:20.382Z",
            "dtTeardownStarted": None,
            "dtTeardownFinished": None,
            "dtDeleted": None,
            "shutdownTimeout": 8,
            "jobId": 20162,
            "isPublic": False,
            "isPreemptible": True,
            "cpuHostname": "gradient-host-1567167274",
            "cpuCount": 1,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "1783380 kB",
            "gpuName": None,
            "gpuSerial": None,
            "gpuDevice": None,
            "gpuDriver": None,
            "gpuCount": None,
            "gpuMem": None,
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1810
        },
        {
            "name": "some_notebook_name",
            "handle": "njmq1zju",
            "jobHandle": "jd35vd65dkqch",
            "project": "Notebook-some_notebook_name",
            "projectHandle": "prflq2sy0",
            "state": "Error",
            "token": None,
            "container": "None",
            "containerUrl": "None",
            "baseContainer": "None",
            "baseContainerUrl": "None",
            "vmType": "G1",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "njmq1zju.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": "Error pulling container during provisioning for job jd35vd65dkqch: Error pulling image 'None': Error response from daemon: Get https://registry-1.docker.io/v2/library/None/manifests/latest: unauthorized: incorrect username or password",
            "dtCreated": "2019-08-30T12:14:32.296Z",
            "dtModified": "2019-08-30T12:14:32.296Z",
            "dtProvisioningStarted": "2019-08-30T12:16:08.347Z",
            "dtProvisioningFinished": None,
            "dtStarted": None,
            "dtFinished": "2019-08-30T12:16:09.132Z",
            "dtTeardownStarted": None,
            "dtTeardownFinished": None,
            "dtDeleted": None,
            "shutdownTimeout": 8,
            "jobId": 20161,
            "isPublic": False,
            "isPreemptible": True,
            "cpuHostname": "gradient-host-1567167274",
            "cpuCount": 1,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "1783380 kB",
            "gpuName": None,
            "gpuSerial": None,
            "gpuDevice": None,
            "gpuDriver": None,
            "gpuCount": None,
            "gpuMem": None,
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1809
        },
        {
            "name": "some_notebook_name",
            "handle": "nfcuwqu5",
            "jobHandle": "je2cmiigxwhy0",
            "project": "Notebook-some_notebook_name",
            "projectHandle": "prl9nu5p7",
            "state": "Error",
            "token": None,
            "container": "some_name",
            "containerUrl": "some_name",
            "baseContainer": "some_name",
            "baseContainerUrl": "some_name",
            "vmType": "G1",
            "cluster": "PS Notebooks on GCP",
            "clusterId": "clmtkpnm2",
            "fqdn": "nfcuwqu5.dgradient.paperspace.com",
            "startedByUser": "first last",
            "startedByUserId": "ukgvw4i8",
            "namespace": "username",
            "parentJobId": None,
            "jobError": "Error pulling container during provisioning for job je2cmiigxwhy0: Error pulling image 'some_name': Error response from daemon: Get https://registry-1.docker.io/v2/library/some_name/manifests/latest: unauthorized: incorrect username or password",
            "dtCreated": "2019-08-30T12:13:30.657Z",
            "dtModified": "2019-08-30T12:13:30.657Z",
            "dtProvisioningStarted": "2019-08-30T12:15:11.388Z",
            "dtProvisioningFinished": None,
            "dtStarted": None,
            "dtFinished": "2019-08-30T12:15:12.207Z",
            "dtTeardownStarted": None,
            "dtTeardownFinished": None,
            "dtDeleted": None,
            "shutdownTimeout": 8,
            "jobId": 20160,
            "isPublic": False,
            "isPreemptible": True,
            "cpuHostname": "gradient-host-1567167224",
            "cpuCount": 1,
            "cpuModel": "Intel(R) Xeon(R) CPU @ 2.30GHz",
            "cpuFlags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities",
            "cpuMem": "1783380 kB",
            "gpuName": None,
            "gpuSerial": None,
            "gpuDevice": None,
            "gpuDriver": None,
            "gpuCount": None,
            "gpuMem": None,
            "tpuType": None,
            "tpuName": None,
            "tpuGrpcUrl": None,
            "tpuTFVersion": None,
            "tpuDatasetDir": None,
            "tpuModelDir": None,
            "id": 1808
        }
    ],
    "availableMachines": [
        {
            "vmTypeId": 5,
            "clusterId": 1,
            "isAvailable": False,
            "isPreemptible": False,
            "showDisabled": False,
            "numActiveNodes": "0",
            "numAvailableNodes": "0",
            "id": 11,
            "cluster": {
                "name": "PS Notebooks",
                "type": 1,
                "regionId": 1,
                "showDisabled": False,
                "dtCreated": "2017-11-03T19:09:41.077Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "cls28l0qm",
                "cloud": None,
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 1
            }
        },
        {
            "vmTypeId": 7,
            "clusterId": 1,
            "isAvailable": True,
            "isPreemptible": False,
            "showDisabled": False,
            "numActiveNodes": "1",
            "numAvailableNodes": "1",
            "id": 15,
            "cluster": {
                "name": "PS Notebooks",
                "type": 1,
                "regionId": 1,
                "showDisabled": False,
                "dtCreated": "2017-11-03T19:09:41.077Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "cls28l0qm",
                "cloud": None,
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 1
            }
        },
        {
            "vmTypeId": 20,
            "clusterId": 3,
            "isAvailable": True,
            "isPreemptible": False,
            "showDisabled": False,
            "numActiveNodes": "2",
            "numAvailableNodes": "0",
            "id": 7,
            "cluster": {
                "name": "PS Notebooks on GCP",
                "type": 1,
                "regionId": 4,
                "showDisabled": False,
                "dtCreated": "2018-03-02T18:27:16.323Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "clmtkpnm2",
                "cloud": "gcp",
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 3
            }
        },
        {
            "vmTypeId": 20,
            "clusterId": 3,
            "isAvailable": True,
            "isPreemptible": True,
            "showDisabled": False,
            "numActiveNodes": "2",
            "numAvailableNodes": "0",
            "id": 6,
            "cluster": {
                "name": "PS Notebooks on GCP",
                "type": 1,
                "regionId": 4,
                "showDisabled": False,
                "dtCreated": "2018-03-02T18:27:16.323Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "clmtkpnm2",
                "cloud": "gcp",
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 3
            }
        },
        {
            "vmTypeId": 21,
            "clusterId": 3,
            "isAvailable": True,
            "isPreemptible": True,
            "showDisabled": False,
            "numActiveNodes": "0",
            "numAvailableNodes": "0",
            "id": 22,
            "cluster": {
                "name": "PS Notebooks on GCP",
                "type": 1,
                "regionId": 4,
                "showDisabled": False,
                "dtCreated": "2018-03-02T18:27:16.323Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "clmtkpnm2",
                "cloud": "gcp",
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 3
            }
        },
        {
            "vmTypeId": 21,
            "clusterId": 3,
            "isAvailable": True,
            "isPreemptible": False,
            "showDisabled": False,
            "numActiveNodes": "0",
            "numAvailableNodes": "0",
            "id": 23,
            "cluster": {
                "name": "PS Notebooks on GCP",
                "type": 1,
                "regionId": 4,
                "showDisabled": False,
                "dtCreated": "2018-03-02T18:27:16.323Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "clmtkpnm2",
                "cloud": "gcp",
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 3
            }
        },
        {
            "vmTypeId": 25,
            "clusterId": 3,
            "isAvailable": True,
            "isPreemptible": False,
            "showDisabled": False,
            "numActiveNodes": "1",
            "numAvailableNodes": "0",
            "id": 27,
            "cluster": {
                "name": "PS Notebooks on GCP",
                "type": 1,
                "regionId": 4,
                "showDisabled": False,
                "dtCreated": "2018-03-02T18:27:16.323Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "clmtkpnm2",
                "cloud": "gcp",
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 3
            }
        },
        {
            "vmTypeId": 25,
            "clusterId": 3,
            "isAvailable": True,
            "isPreemptible": True,
            "showDisabled": False,
            "numActiveNodes": "1",
            "numAvailableNodes": "0",
            "id": 26,
            "cluster": {
                "name": "PS Notebooks on GCP",
                "type": 1,
                "regionId": 4,
                "showDisabled": False,
                "dtCreated": "2018-03-02T18:27:16.323Z",
                "dtModified": "2019-05-29T15:56:16.039Z",
                "dtDeleted": None,
                "handle": "clmtkpnm2",
                "cloud": "gcp",
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 3
            }
        },
        {
            "vmTypeId": 31,
            "clusterId": 90,
            "isAvailable": True,
            "isPreemptible": False,
            "showDisabled": False,
            "numActiveNodes": "1",
            "numAvailableNodes": "1",
            "id": 1,
            "cluster": {
                "name": "Free Public Notebooks",
                "type": 1,
                "regionId": 2,
                "showDisabled": False,
                "dtCreated": "2019-06-18T23:33:58.997Z",
                "dtModified": "2019-08-12T17:06:19.492Z",
                "dtDeleted": None,
                "handle": "cltwhzxx6",
                "cloud": None,
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 90
            }
        },
        {
            "vmTypeId": 32,
            "clusterId": 90,
            "isAvailable": True,
            "isPreemptible": False,
            "showDisabled": False,
            "numActiveNodes": "1",
            "numAvailableNodes": "1",
            "id": 12,
            "cluster": {
                "name": "Free Public Notebooks",
                "type": 1,
                "regionId": 2,
                "showDisabled": False,
                "dtCreated": "2019-06-18T23:33:58.997Z",
                "dtModified": "2019-08-12T17:06:19.492Z",
                "dtDeleted": None,
                "handle": "cltwhzxx6",
                "cloud": None,
                "isDeleted": False,
                "isPrivate": False,
                "isDefault": False,
                "fqdn": None,
                "id": 90
            }
        }
    ],
    "total": 9,
    "runningTotal": 2,
    "displayTotal": 9
}

GET_PRESIGNED_URL_FOR_S3_BUCKET_RESPONSE_JSON = {
    "data": {
        "bucket_name": "ps-projects",
        "fields": {
            "AWSAccessKeyId": "SOME_AWS_ACCESS_KEY_ID",
            "key": "some/path/to/file/demo.zip",
            "policy": "base64policy=",
            "signature": "base64signature="
        },
        "url": "https://ps-projects.s3.amazonaws.com/"
    },
    "message": "success"
}

DELETE_MODEL_404_RESPONSE_JSON = {
    "error": {
        "name": "Error",
        "status": 404,
        "message": "Unable to find model",
    },
}

MODEL_CREATE_RESPONSE_JSON_V2 = {
    "id": "some_model_id",
    "projectId": None,
    "updatedByUserId": "ukgvw4i8",
    "updatedByUserEmail": "asd@paperspace.com",
    "modelType": "Custom",
    "name": "some_name",
    "tag": None,
    "summary": None,
    "detail": None,
    "params": None,
    "url": None,
    "notes": None,
    "isDeleted": False,
    "isPublic": False,
    "dtCreated": "2020-04-01T14:15:39.371Z",
    "dtModified": "2020-04-01T14:15:39.371Z",
    "dtUploaded": None,
    "dtDeleted": None,
    "modelPath": None,
    "deploymentState": None,
    "tags": None
}

MODEL_UPLOAD_GET_PRESIGNED_URL_RESPONSE = "https://ps-customstorage-development.s3.amazonaws.com/teo6raui0/models/" \
                                          "moslrdsp1q4z4a2/keton.txt?AWSAccessKeyId=AKIAVWO7J5OJXEKIB7EJ&Content-Typ" \
                                          "e=text%2Fplain&Expires=1585779340&Signature=82UPgvg0yBayLJCLMiNq6jc4mys%3D"

MODEL_UPLOAD_RESPONSE_JSON = {
    "id": "some_model_id",
    "projectId": None,
    "updatedByUserId": "ukgvw4i8",
    "updatedByUserEmail": "some_email@paperspace.com",
    "modelType": "Tensorflow",
    "name": "some_name",
    "tag": None,
    "summary": {"key": "value"},
    "detail": None,
    "params": None,
    "url": "s3://ps-projects-development/teo6raui0/models/some_model_id/saved_model.pb",
    "notes": "some notes",
    "isDeleted": False,
    "isPublic": False,
    "dtCreated": "2019-11-26T13:33:11.001Z", "dtModified": "2019-11-26T13:33:11.001Z",
    "dtUploaded": None,
    "dtDeleted": None,
    "modelPath": None,
    "deploymentState": None,
}

MODEL_DETAILS_RESPONSE_JSON = {
    "modelList": [
        {
            "id": "some_id",
            "projectId": "some_project_id",
            "updatedByUserId": "some_user_id",
            "updatedByUserEmail": "paperspace@paperspace.com",
            "modelType": "Tensorflow",
            "name": "some_name",
            "tag": None,
            "summary": None,
            "detail": None,
            "params": None,
            "url": "s3://ps-projects-development/asdf/some_project_id/some_experiment_id/model",
            "notes": None,
            "isDeleted": False,
            "isPublic": False,
            "dtCreated": "2019-12-13T23:00:26.077Z",
            "dtModified": "2019-12-13T23:00:26.077Z",
            "dtUploaded": None,
            "dtDeleted": None,
            "modelPath": None,
            "deploymentState": "Stopped"
        }
    ],
    "total": 96,
    "displayTotal": 1
}

MODEL_DETAILS_RESPONSE_JSON_WITH_TAGS = {
    "modelList": [
        {
            "id": "some_id",
            "projectId": "some_project_id",
            "updatedByUserId": "some_user_id",
            "updatedByUserEmail": "paperspace@paperspace.com",
            "modelType": "Tensorflow",
            "name": "some_name",
            "tag": None,
            "tags": [
                "tag1",
                "tag2"
            ],
            "summary": None,
            "detail": None,
            "params": None,
            "url": "s3://ps-projects-development/asdf/some_project_id/some_experiment_id/model",
            "notes": None,
            "isDeleted": False,
            "isPublic": False,
            "dtCreated": "2019-12-13T23:00:26.077Z",
            "dtModified": "2019-12-13T23:00:26.077Z",
            "dtUploaded": None,
            "dtDeleted": None,
            "modelPath": None,
            "deploymentState": "Stopped"
        }
    ],
    "total": 96,
    "displayTotal": 1
}

LIST_MODEL_FILES_RESPONSE_JSON = [
    {
        "file": "hello.txt",
        "url": "https://ps-projects.s3.amazonaws.com/some/path/model/hello.txt?AWSAccessKeyId=some_aws_access_key_id&Expires=713274132&Signature=7CT5k6buEmZe5k5E7g6BXMs2xV4%3D&response-content-disposition=attachment%3Bfilename%3D%22hello.txt%22&x-amz-security-token=some_amz_security_token"
    },
    {
        "file": "hello2.txt",
        "url": "https://ps-projects.s3.amazonaws.com/some/path/model/hello2.txt?AWSAccessKeyId=some_aws_access_key_id&Expires=713274132&Signature=L1lI47cNyiROzdYkf%2FF3Cm3165E%3D&response-content-disposition=attachment%3Bfilename%3D%22hello2.txt%22&x-amz-security-token=some_amz_security_token"
    },
    {
        "file": "keton/elo.txt",
        "url": "https://ps-projects.s3.amazonaws.com/some/path/model/keton/elo.txt?AWSAccessKeyId=some_aws_access_key_id&Expires=713274132&Signature=tHriojGx03S%2FKkVGQGVI5CQRFTo%3D&response-content-disposition=attachment%3Bfilename%3D%22elo.txt%22&x-amz-security-token=some_amz_security_token"
    }
]

GET_CLUSTER_DETAILS_RESPONSE = {
    "id": "some_cluster_id",
    "name": "EKS testing",
    "type": "Kubernetes Processing Site",
    "region": "Private",
    "cloud": "aws",
    "teamId": "some_team_id",
    "isDefault": False,
    "dtCreated": "2019-11-21T07:27:37.010Z",
    "dtModified": "2019-11-21T18:12:27.723Z",
    "clusterId": 1,
    "isPrivate": True,
    "modelName": "team",
    "modelId": 1,
    "nodes": [
        {
            "id": "cmsq4u0gf0m971f",
            "name": "default",
            "clusterId": "cluwffvkb",
            "activeJobId": None,
            "machineId": None,
            "dtCreated": "2019-11-21T10:06:27.602Z",
            "dtModified": "2019-11-21T10:06:27.602Z",
            "dtDeleted": None,
            "dtHeartbeat": None,
            "nodeAttrs": None
        }
    ]
}
GET_V1_CLUSTER_DETAILS_RESPONSE = {
    "id": "some_cluster_id",
    "name": "EKS testing",
    "type": "Job Cluster",
    "region": "Private",
    "cloud": "aws",
    "teamId": "some_team_id",
    "isDefault": False,
    "dtCreated": "2019-11-21T07:27:37.010Z",
    "dtModified": "2019-11-21T18:12:27.723Z",
    "clusterId": 1,
    "isPrivate": True,
    "modelName": "team",
    "modelId": 1,
    "nodes": [
        {
            "id": "some_node_id",
            "name": "default",
            "clusterId": "some_cluster_id",
            "activeJobId": None,
            "machineId": None,
            "dtCreated": "2019-11-21T10:06:27.602Z",
            "dtModified": "2019-11-21T10:06:27.602Z",
            "dtDeleted": None,
            "dtHeartbeat": None,
            "nodeAttrs": None
        }
    ]
}

DETAILS_OF_PROJECT = {
    "data": [
        {
            "name": "some_name",
            "handle": "some_id",
            "dtCreated": "2020-02-07T11:43:34.335Z",
            "dtDeleted": None,
            "lastJobSeqNum": 44,
            "repoNodeId": None,
            "repoName": None,
            "repoUrl": None,
            "tags": None,
            "buildPullRequests": True,
            "buildForks": False,
            "buildBranches": "default",
        }
    ],
    "meta": {
        "where": {
            "handle": "some_id"
        },
        "totalItems": 1
    },
    "tagFilter": []
}

DETAILS_OF_PROJECT_WITH_TAGS = {
    "data": [
        {
            "name": "some_name",
            "handle": "some_id",
            "dtCreated": "2020-02-07T11:43:34.335Z",
            "dtDeleted": None,
            "lastJobSeqNum": 44,
            "repoNodeId": None,
            "repoName": None,
            "repoUrl": None,
            "tags": [
                "tag1",
                "tag2"
            ],
            "buildPullRequests": True,
            "buildForks": False,
            "buildBranches": "default",
        }
    ],
    "meta": {
        "where": {
            "handle": "some_id"
        },
        "totalItems": 1
    },
    "tagFilter": []
}

EXAMPLE_CLUSTERS_LIST_RESPONSE = [
    {
        "id": "cluster_id_1",
        "name": "cluster name 1",
        "type": "Job Cluster",
        "region": "Private",
        "cloud": "private",
        "teamId": "team_id",
        "isDefault": True,
        "dtCreated": "2019-07-05T23:28:17.416Z",
        "dtModified": "2019-07-05T23:28:17.416Z",
        "clusterId": 91,
        "isPrivate": True,
        "modelName": "team",
        "modelId": 1170
    },
    {
        "id": "cluster_id_2",
        "name": "cluster name 2",
        "type": "Kubernetes Processing Site",
        "region": "Private",
        "cloud": "aws",
        "teamId": "team_id",
        "isDefault": False,
        "dtCreated": "2019-07-22T14:50:10.170Z",
        "dtModified": "2019-11-21T18:12:27.723Z",
        "clusterId": 92,
        "isPrivate": True,
        "modelName": "team",
        "modelId": 1170
    },
    {
        "id": "cluster_id_3",
        "name": "cluster name 3",
        "type": "Job Cluster",
        "region": "Private",
        "cloud": "gcp",
        "teamId": "team_id",
        "isDefault": False,
        "dtCreated": "2019-10-29T18:42:50.985Z",
        "dtModified": "2019-11-21T18:12:27.723Z",
        "clusterId": 100,
        "isPrivate": True,
        "modelName": "team",
        "modelId": 1170
    }
]

LIMITED_EXAMPLE_CLUSTERS_LIST_RESPONSE = [
    {
        "id": "cluster_id_1",
        "name": "cluster name 1",
        "type": "Job Cluster",
        "region": "Private",
        "cloud": "private",
        "teamId": "team_id",
        "isDefault": True,
        "dtCreated": "2019-07-05T23:28:17.416Z",
        "dtModified": "2019-07-05T23:28:17.416Z",
        "clusterId": 91,
        "isPrivate": True,
        "modelName": "team",
        "modelId": 1170
    },
    {
        "id": "cluster_id_2",
        "name": "cluster name 2",
        "type": "Kubernetes Processing Site",
        "region": "Private",
        "cloud": "aws",
        "teamId": "team_id",
        "isDefault": False,
        "dtCreated": "2019-07-22T14:50:10.170Z",
        "dtModified": "2019-11-21T18:12:27.723Z",
        "clusterId": 92,
        "isPrivate": True,
        "modelName": "team",
        "modelId": 1170
    }
]

LIST_OF_VM_MACHINE_TYPES = {
    "92": [
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 35,
            "capacityId": 21,
            "vmType": {
                "label": "c5.xlarge",
                "kind": "aws-cpu",
                "cpus": 4,
                "ram": "8589934592",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:12:41.506Z",
                "dtModified": "2019-08-28T17:40:50.773Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "small",
                "id": 35,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 35,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:32:41.602Z",
                        "isPreemptible": False,
                        "id": 131,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clqr4b0ox",
                    "name": "KPS Jobs",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-07-22T14:50:10.170Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 92,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 36,
            "capacityId": 22,
            "vmType": {
                "label": "c5.4xlarge",
                "kind": "aws-cpu",
                "cpus": 16,
                "ram": "34359738368",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:14:06.425Z",
                "dtModified": "2019-08-28T17:40:50.773Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "medium",
                "id": 36,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 36,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:32:41.602Z",
                        "isPreemptible": False,
                        "id": 132,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clqr4b0ox",
                    "name": "KPS Jobs",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-07-22T14:50:10.170Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 92,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 38,
            "capacityId": 23,
            "vmType": {
                "label": "p2.xlarge",
                "kind": "aws-gpu",
                "cpus": 4,
                "ram": "65498251264",
                "gpuModelId": 11,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "small",
                "id": 38,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla K80",
                    "gpuGroupId": 8,
                    "memInBytes": "12884901888",
                    "memInMb": 12288,
                    "memInGb": "12",
                    "id": 11
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 38,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:05.626Z",
                        "isPreemptible": False,
                        "id": 134,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clqr4b0ox",
                    "name": "KPS Jobs",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-07-22T14:50:10.170Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 92,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 39,
            "capacityId": 24,
            "vmType": {
                "label": "p3.2xlarge",
                "kind": "aws-gpu",
                "cpus": 8,
                "ram": "65498251264",
                "gpuModelId": 10,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "medium",
                "id": 39,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla V100",
                    "gpuGroupId": 7,
                    "memInBytes": "17179869184",
                    "memInMb": 16384,
                    "memInGb": "16",
                    "id": 10
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 39,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:05.626Z",
                        "isPreemptible": False,
                        "id": 135,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clqr4b0ox",
                    "name": "KPS Jobs",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-07-22T14:50:10.170Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 92,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 40,
            "capacityId": 25,
            "vmType": {
                "label": "p3.16xlarge",
                "kind": "aws-gpu",
                "cpus": 64,
                "ram": "523986010112",
                "gpuModelId": 10,
                "gpuCount": 8,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "large",
                "id": 40,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla V100",
                    "gpuGroupId": 7,
                    "memInBytes": "17179869184",
                    "memInMb": 16384,
                    "memInGb": "16",
                    "id": 10
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 40,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:14.282Z",
                        "isPreemptible": False,
                        "id": 136,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clqr4b0ox",
                    "name": "KPS Jobs",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-07-22T14:50:10.170Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 92,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        }
    ],
    "102": [
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 65,
            "capacityId": 32,
            "vmType": {
                "label": "Wolfpass-CPU",
                "kind": "cpu",
                "cpus": 24,
                "ram": "34359738368",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-11-11T19:53:21.298Z",
                "dtModified": "2019-11-19T19:09:03.288Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "small",
                "id": 65,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 65,
                        "type": "hourly",
                        "usageRateId": 18,
                        "dtCreated": "2019-11-11T19:57:04.870Z",
                        "isPreemptible": False,
                        "id": 150,
                        "usageRate": {
                            "description": "VIP",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "VIP",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": False,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 18
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clfe0kr2p",
                    "name": "Intel Wolfpass KPS",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "intelwolfpass",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-11T16:34:29.495Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 102,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        }
    ],
    "103": [
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 35,
            "capacityId": 33,
            "vmType": {
                "label": "c5.xlarge",
                "kind": "aws-cpu",
                "cpus": 4,
                "ram": "8589934592",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:12:41.506Z",
                "dtModified": "2019-08-28T17:40:50.773Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "small",
                "id": 35,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 35,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:32:41.602Z",
                        "isPreemptible": False,
                        "id": 131,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "cluwffvkb",
                    "name": "EKS testing",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-21T07:27:37.010Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 103,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 36,
            "capacityId": 34,
            "vmType": {
                "label": "c5.4xlarge",
                "kind": "aws-cpu",
                "cpus": 16,
                "ram": "34359738368",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:14:06.425Z",
                "dtModified": "2019-08-28T17:40:50.773Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "medium",
                "id": 36,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 36,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:32:41.602Z",
                        "isPreemptible": False,
                        "id": 132,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "cluwffvkb",
                    "name": "EKS testing",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-21T07:27:37.010Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 103,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 37,
            "capacityId": 35,
            "vmType": {
                "label": "c5.24xlarge",
                "kind": "aws-cpu",
                "cpus": 94,
                "ram": "206158430208",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:14:06.425Z",
                "dtModified": "2019-08-28T17:40:50.773Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "large",
                "id": 37,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 37,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:05.626Z",
                        "isPreemptible": False,
                        "id": 133,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "cluwffvkb",
                    "name": "EKS testing",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-21T07:27:37.010Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 103,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 39,
            "capacityId": 36,
            "vmType": {
                "label": "p3.2xlarge",
                "kind": "aws-gpu",
                "cpus": 8,
                "ram": "65498251264",
                "gpuModelId": 10,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "medium",
                "id": 39,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla V100",
                    "gpuGroupId": 7,
                    "memInBytes": "17179869184",
                    "memInMb": 16384,
                    "memInGb": "16",
                    "id": 10
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 39,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:05.626Z",
                        "isPreemptible": False,
                        "id": 135,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "cluwffvkb",
                    "name": "EKS testing",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-21T07:27:37.010Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 103,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 40,
            "capacityId": 37,
            "vmType": {
                "label": "p3.16xlarge",
                "kind": "aws-gpu",
                "cpus": 64,
                "ram": "523986010112",
                "gpuModelId": 10,
                "gpuCount": 8,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "large",
                "id": 40,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla V100",
                    "gpuGroupId": 7,
                    "memInBytes": "17179869184",
                    "memInMb": 16384,
                    "memInGb": "16",
                    "id": 10
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 40,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:14.282Z",
                        "isPreemptible": False,
                        "id": 136,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "cluwffvkb",
                    "name": "EKS testing",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-21T07:27:37.010Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 103,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 66,
            "capacityId": 38,
            "vmType": {
                "label": "c5.xlarge",
                "kind": "eks-cpu",
                "cpus": 4,
                "ram": "8589934592",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-11-27T11:08:38.641Z",
                "dtModified": "2019-11-27T11:08:38.641Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "small",
                "id": 66,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 66,
                        "type": "hourly",
                        "usageRateId": 18,
                        "dtCreated": "2019-11-27T11:59:58.059Z",
                        "isPreemptible": False,
                        "id": 151,
                        "usageRate": {
                            "description": "VIP",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "VIP",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": False,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 18
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "cluwffvkb",
                    "name": "EKS testing",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-21T07:27:37.010Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 103,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 66,
            "capacityId": 39,
            "vmType": {
                "label": "c5.xlarge",
                "kind": "eks-cpu",
                "cpus": 4,
                "ram": "8589934592",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-11-27T11:08:38.641Z",
                "dtModified": "2019-11-27T11:08:38.641Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "small",
                "id": 66,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 66,
                        "type": "hourly",
                        "usageRateId": 18,
                        "dtCreated": "2019-11-27T11:59:58.059Z",
                        "isPreemptible": False,
                        "id": 151,
                        "usageRate": {
                            "description": "VIP",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "VIP",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": False,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 18
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "cluwffvkb",
                    "name": "EKS testing",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2019-11-21T07:27:37.010Z",
                    "dtModified": "2020-02-28T20:58:26.134Z",
                    "clusterId": 103,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        }
    ],
    "175": [
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 35,
            "capacityId": 134,
            "vmType": {
                "label": "c5.xlarge",
                "kind": "aws-cpu",
                "cpus": 4,
                "ram": "8589934592",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:12:41.506Z",
                "dtModified": "2019-08-28T17:40:50.773Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "small",
                "id": 35,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 35,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:32:41.602Z",
                        "isPreemptible": False,
                        "id": 131,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clrvkwq6l",
                    "name": "test",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2020-03-09T17:15:08.080Z",
                    "dtModified": "2020-03-09T17:15:08.080Z",
                    "clusterId": 175,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 36,
            "capacityId": 135,
            "vmType": {
                "label": "c5.4xlarge",
                "kind": "aws-cpu",
                "cpus": 16,
                "ram": "34359738368",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:14:06.425Z",
                "dtModified": "2019-08-28T17:40:50.773Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "medium",
                "id": 36,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 36,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:32:41.602Z",
                        "isPreemptible": False,
                        "id": 132,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clrvkwq6l",
                    "name": "test",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2020-03-09T17:15:08.080Z",
                    "dtModified": "2020-03-09T17:15:08.080Z",
                    "clusterId": 175,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 38,
            "capacityId": 136,
            "vmType": {
                "label": "p2.xlarge",
                "kind": "aws-gpu",
                "cpus": 4,
                "ram": "65498251264",
                "gpuModelId": 11,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "small",
                "id": 38,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla K80",
                    "gpuGroupId": 8,
                    "memInBytes": "12884901888",
                    "memInMb": 12288,
                    "memInGb": "12",
                    "id": 11
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 38,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:05.626Z",
                        "isPreemptible": False,
                        "id": 134,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clrvkwq6l",
                    "name": "test",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2020-03-09T17:15:08.080Z",
                    "dtModified": "2020-03-09T17:15:08.080Z",
                    "clusterId": 175,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 39,
            "capacityId": 137,
            "vmType": {
                "label": "p3.2xlarge",
                "kind": "aws-gpu",
                "cpus": 8,
                "ram": "65498251264",
                "gpuModelId": 10,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "medium",
                "id": 39,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla V100",
                    "gpuGroupId": 7,
                    "memInBytes": "17179869184",
                    "memInMb": 16384,
                    "memInGb": "16",
                    "id": 10
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 39,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:05.626Z",
                        "isPreemptible": False,
                        "id": 135,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clrvkwq6l",
                    "name": "test",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2020-03-09T17:15:08.080Z",
                    "dtModified": "2020-03-09T17:15:08.080Z",
                    "clusterId": 175,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 40,
            "capacityId": 138,
            "vmType": {
                "label": "p3.16xlarge",
                "kind": "aws-gpu",
                "cpus": 64,
                "ram": "523986010112",
                "gpuModelId": 10,
                "gpuCount": 8,
                "internalDescription": None,
                "dtCreated": "2019-07-22T15:20:22.108Z",
                "dtModified": "2019-08-28T17:40:50.779Z",
                "isPreemptible": False,
                "deploymentType": "gpu",
                "deploymentSize": "large",
                "id": 40,
                "gpuModel": {
                    "model": "passthrough",
                    "label": "Tesla V100",
                    "gpuGroupId": 7,
                    "memInBytes": "17179869184",
                    "memInMb": 16384,
                    "memInGb": "16",
                    "id": 10
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 40,
                        "type": "hourly",
                        "usageRateId": 10,
                        "dtCreated": "2019-07-22T15:33:14.282Z",
                        "isPreemptible": False,
                        "id": 136,
                        "usageRate": {
                            "description": "Employee",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "Employee",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": True,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 10
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clrvkwq6l",
                    "name": "test",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2020-03-09T17:15:08.080Z",
                    "dtModified": "2020-03-09T17:15:08.080Z",
                    "clusterId": 175,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        },
        {
            "showDisabled": False,
            "isAvailable": True,
            "isPreemptible": False,
            "vmTypeId": 66,
            "capacityId": 139,
            "vmType": {
                "label": "c5.xlarge",
                "kind": "eks-cpu",
                "cpus": 4,
                "ram": "8589934592",
                "gpuModelId": 6,
                "gpuCount": 1,
                "internalDescription": None,
                "dtCreated": "2019-11-27T11:08:38.641Z",
                "dtModified": "2019-11-27T11:08:38.641Z",
                "isPreemptible": False,
                "deploymentType": "cpu",
                "deploymentSize": "small",
                "id": 66,
                "gpuModel": {
                    "model": "None",
                    "label": "None",
                    "gpuGroupId": 3,
                    "memInBytes": "0",
                    "memInMb": 0,
                    "memInGb": "0",
                    "id": 6
                },
                "availableTemplatesWithOperatingSystems": [],
                "availableRegions": [],
                "permissions": [],
                "defaultUsageRates": [
                    {
                        "vmTypeId": 66,
                        "type": "hourly",
                        "usageRateId": 18,
                        "dtCreated": "2019-11-27T11:59:58.059Z",
                        "isPreemptible": False,
                        "id": 151,
                        "usageRate": {
                            "description": "VIP",
                            "rate": "0.00",
                            "type": "monthly",
                            "gpuModelId": 1,
                            "rateHourly": "0.00",
                            "rateMonthly": "0.00",
                            "label": "VIP",
                            "period": "monthly",
                            "kind": "air",
                            "isEarlyAccess": False,
                            "isEmployeeOnly": False,
                            "numCpus": 2,
                            "ramInBytes": "4294967296",
                            "id": 18
                        }
                    }
                ],
                "defaultUsageRateOverrides": []
            },
            "clusters": [
                {
                    "id": "clrvkwq6l",
                    "name": "test",
                    "type": "Kubernetes Processing Site",
                    "region": "Private",
                    "cloud": "aws",
                    "teamId": "teo6raui0",
                    "isDefault": False,
                    "dtCreated": "2020-03-09T17:15:08.080Z",
                    "dtModified": "2020-03-09T17:15:08.080Z",
                    "clusterId": 175,
                    "isPrivate": True,
                    "modelName": "team",
                    "modelId": 1170
                }
            ]
        }
    ]
}

NOTEBOOKS_METRICS_GET_RESPONSE = {
    "handle": "npmnnm6e",
    "object_type": "notebook",
    "charts": {
        "cpuPercentage": {
            "npmnnm6e": [
                {"time_stamp": 1587993000, "value": "0"},
                {"time_stamp": 1587993030, "value": "0"},
                {"time_stamp": 1587993060, "value": "0"},
                {"time_stamp": 1587993090, "value": "0"},
                {"time_stamp": 1587993120, "value": "0"},
                {"time_stamp": 1587993150, "value": "0"},
                {"time_stamp": 1587993180, "value": "0"},
                {"time_stamp": 1587993210, "value": "0"},
                {"time_stamp": 1587993240, "value": "0"},
                {"time_stamp": 1587993270, "value": "0"},
                {"time_stamp": 1587993300, "value": "0"},
                {"time_stamp": 1587993330, "value": "0"},
                {"time_stamp": 1587993360, "value": "0"},
            ],
        },
        "memoryUsage": {
            "npmnnm6e": [
                {"time_stamp": 1587992970, "value": "0"},
                {"time_stamp": 1587993000, "value": "782336"},
                {"time_stamp": 1587993030, "value": "782336"},
                {"time_stamp": 1587993060, "value": "782336"},
                {"time_stamp": 1587993090, "value": "782336"},
                {"time_stamp": 1587993120, "value": "782336"},
                {"time_stamp": 1587993150, "value": "782336"},
                {"time_stamp": 1587993180, "value": "782336"},
                {"time_stamp": 1587993210, "value": "782336"},
                {"time_stamp": 1587993240, "value": "782336"},
                {"time_stamp": 1587993270, "value": "782336"},
                {"time_stamp": 1587993300, "value": "782336"},
                {"time_stamp": 1587993330, "value": "782336"},
                {"time_stamp": 1587993360, "value": "782336"},
            ],
        },
    },
}

NOTEBOOKS_METRICS_GET_RESPONSE_WHEN_NO_METRICS_WERE_FOUND = {
    "handle": "nrwed38p",
    "object_type": "notebook",
    "charts": {"cpuPercentage": None, "memoryUsage": None},
}

DEPLOYMENTS_LOGS_RESPONSE = [
    {
        "jobId": "deshj1l4nuw6sd1",
        "line": 1,
        "timestamp": "2020-05-11T11:27:56.552Z",
        "message": "line1\n",
        "instanceName": {
            "String": "deshj1l4nuw6sd1-1-artifact-1-5nd94",
            "Valid": True
        },
        "uuid": {
            "String": "1ef5d86b-d05e-4610-8f81-b42b556cede7",
            "Valid": True
        },
        "instanceCount": {
            "Int64": 1,
            "Valid": True
        }
    },
    {
        "jobId": "deshj1l4nuw6sd1",
        "line": 2,
        "timestamp": "2020-05-11T11:27:56.552Z",
        "message": "line2\n",
        "instanceName": {
            "String": "deshj1l4nuw6sd1-1-artifact-1-5nd94",
            "Valid": True
        },
        "uuid": {
            "String": "1ef5d86b-d05e-4610-8f81-b42b556cede7",
            "Valid": True
        },
        "instanceCount": {
            "Int64": 1,
            "Valid": True
        }
    },
    {
        "jobId": "deshj1l4nuw6sd1",
        "line": 3,
        "timestamp": "2020-05-11T11:27:56.557Z",
        "message": "line3",
        "instanceName": {
            "String": "deshj1l4nuw6sd1-1-artifact-1-5nd94",
            "Valid": True
        },
        "uuid": {
            "String": "1ef5d86b-d05e-4610-8f81-b42b556cede7",
            "Valid": True
        },
        "instanceCount": {
            "Int64": 1,
            "Valid": True
        }
    },
    {
        "jobId": "deshj1l4nuw6sd1",
        "line": 4,
        "timestamp": "2020-05-11T11:27:56.558Z",
        "message": "PSEOF"
    }
]

LIST_SECRETS_RESPONSE = [
    {
        "name": "aws_access_key_id"
    },
    {
        "name": "aws_secret_access_key"
    }
]

LIST_DATASETS_RESPONSE = [
    {
        "description": None,
        "dtCreated": "2020-10-09T18:34:07.097Z",
        "dtModified": "2020-10-09T18:34:07.097Z",
        "id": "dsttn2y7j1ux882",
        "name": "test1",
        "storageProvider": {
            "config": {
                "accessKey": "AKIAVWO7J5OJV4XSVOPA",
                "bucket": "chris-dev-cluster",
                "secretAccessKey": "********"
            },
            "dtCreated": "2020-10-09T18:17:34.192Z",
            "dtModified": "2020-10-09T18:29:22.368Z",
            "id": "spltautet072md4",
            "name": "test1",
            "type": "s3"
        }
    }
]

SHOW_DATASET_DETAILS_RESPONSE = {
    "description": None,
    "dtCreated": "2020-10-09T18:34:07.097Z",
    "dtModified": "2020-10-09T18:34:07.097Z",
    "id": "dsttn2y7j1ux882",
    "name": "test1",
    "storageProvider": {
        "config": {
            "accessKey": "AKIAVWO7J5OJV4XSVOPA",
            "bucket": "chris-dev-cluster",
            "secretAccessKey": "********"
        },
        "dtCreated": "2020-10-09T18:17:34.192Z",
        "dtModified": "2020-10-09T18:29:22.368Z",
        "id": "spltautet072md4",
        "name": "test1",
        "type": "s3"
    }
}

CREATE_DATASET_RESPONSE = {
    "description": None,
    "dtCreated": "2020-10-09T18:34:07.097Z",
    "dtModified": "2020-10-09T18:34:07.097Z",
    "id": "dsttn2y7j1ux882",
    "name": "test1",
    "storageProvider": {
        "config": {
            "accessKey": "AKIAVWO7J5OJV4XSVOPA",
            "bucket": "chris-dev-cluster",
            "secretAccessKey": "********"
        },
        "dtCreated": "2020-10-09T18:17:34.192Z",
        "dtModified": "2020-10-09T18:29:22.368Z",
        "id": "spltautet072md4",
        "name": "test1",
        "type": "s3"
    }
}

UPDATE_DATASET_RESPONSE = {
    "description": "Test dataset",
    "dtCreated": "2020-10-09T18:34:07.097Z",
    "dtModified": "2020-10-09T18:34:07.097Z",
    "id": "dsttn2y7j1ux882",
    "name": "test1",
    "storageProvider": {
        "config": {
            "accessKey": "AKIAVWO7J5OJV4XSVOPA",
            "bucket": "chris-dev-cluster",
            "secretAccessKey": "********"
        },
        "dtCreated": "2020-10-09T18:17:34.192Z",
        "dtModified": "2020-10-09T18:29:22.368Z",
        "id": "spltautet072md4",
        "name": "test1",
        "type": "s3"
    }
}

LIST_DATASET_VERSIONS_RESPONSE = [
    {
        "dtCreated": "2020-10-29T22:56:15.514Z",
        "dtModified": "2020-10-29T22:56:16.213Z",
        "isCommitted": True,
        "message": None,
        "tags": [
            {
                "name": "hello"
            }
        ],
        "version": "1rn19s2"
    }
]

SHOW_DATASET_VERSION_DETAILS_RESPONSE = {
    "dtCreated": "2020-10-29T22:56:15.514Z",
    "dtModified": "2020-10-29T22:56:16.213Z",
    "isCommitted": True,
    "message": None,
    "tags": [
        {
            "name": "hello"
        }
    ],
    "version": "1rn19s2"
}

UPDATE_DATASET_VERSION_RESPONSE = {
    "dtCreated": "2020-10-29T22:56:15.514Z",
    "dtModified": "2020-10-29T23:27:14.955Z",
    "isCommitted": True,
    "message": "Test message",
    "tags": [
        {
            "name": "hello"
        }
    ],
    "version": "1rn19s2"
}

SET_DATASET_VERSION_TAG_RESPONSE = {
    "dtCreated": "2020-10-29T22:57:40.723Z",
    "dtModified": "2020-10-29T23:48:42.948Z",
    "name": "hello",
    "version": {
        "message": "Test message",
        "version": "1rn19s2"
    }
}

LIST_STORAGE_PROVIDERS_RESPONSE = [
    {
        "config": {
            "accessKey": "AKIBAEG7J3OJ24XAV33B",
            "bucket": "bucket",
            "secretAccessKey": "********"
        },
        "dtCreated": "2020-10-09T18:17:34.192Z",
        "dtModified": "2020-10-09T18:29:22.368Z",
        "id": "spltautet072md4",
        "name": "test1",
        "type": "s3"
    }
]

SHOW_STORAGE_PROVIDER_DETAILS_RESPONSE = {
    "config": {
        "accessKey": "AKIBAEG7J3OJ24XAV33B",
        "bucket": "bucket",
        "secretAccessKey": "********"
    },
    "dtCreated": "2020-10-09T18:17:34.192Z",
    "dtModified": "2020-10-09T18:29:22.368Z",
    "id": "spltautet072md4",
    "name": "test1",
    "type": "s3"
}

CREATE_STORAGE_PROVIDER_RESPONSE = {
    "config": {
        "accessKey": "AKIBAEG7J3OJ24XAV33B",
        "bucket": "bucket",
        "secretAccessKey": "********"
    },
    "dtCreated": "2020-10-09T18:17:34.192Z",
    "dtModified": "2020-10-09T18:29:22.368Z",
    "id": "spltautet072md4",
    "name": "test1",
    "type": "s3"
}

UPDATE_STORAGE_PROVIDER_RESPONSE = {
    "config": {
        "accessKey": "AKIBAEG7J3OJ24XAV33B",
        "bucket": "bucket",
        "secretAccessKey": "********"
    },
    "dtCreated": "2020-10-09T18:17:34.192Z",
    "dtModified": "2020-10-09T18:29:22.368Z",
    "id": "spltautet072md4",
    "name": "test2",
    "type": "s3"
}
