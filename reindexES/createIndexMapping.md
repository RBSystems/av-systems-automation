curl -XDELETE 'http://avreports.byu.edu:9200/events_v3'

curl -XPOST 'http://avreports.byu.edu:9200/events_v3' -d '{
    "aliases": {"events_v3":{}},
    "mappings": {
        "system": {
            "properties": {
                "action": {
                    "properties": {
                        "actor": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "device": {
                    "properties": {
                        "description": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "hostname": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "ipAddress": {
                            "type": "ip"
                        },
                        "macAddress": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "eventType": {
                    "type": "string"
                },
                "room": {
                    "dynamic": "true",
                    "properties": {
                        "building": {
                            "type": "string"
                        },
                        "coordinates": {
                            "type": "geo_point"
                        },
                        "floor": {
                            "type": "string"
                        },
                        "roomNumber": {
                            "type": "string"
                        },
                        "room": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "timestamp": {
                    "type": "date",
                    "format": "dateOptionalTime"
                }
            }
        },
        "_default_": {
            "properties": {
                "action": {
                    "properties": {
                        "actor": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "device": {
                    "properties": {
                        "description": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "hostname": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "ipAddress": {
                            "type": "ip"
                        },
                        "macAddress": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "eventType": {
                    "type": "string"
                },
                "room": {
                    "dynamic": "true",
                    "properties": {
                        "building": {
                            "type": "string"
                        },
                        "coordinates": {
                            "type": "geo_point"
                        },
                        "floor": {
                            "type": "string"
                        },
                        "roomNumber": {
                            "type": "string"
                        },
                        "room": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "timestamp": {
                    "type": "date",
                    "format": "dateOptionalTime",
                    "enabled": true,
                    "store": true
                }
            }
        },
        "user": {
            "properties": {
                "action": {
                    "properties": {
                        "actor": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "device": {
                    "properties": {
                        "description": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "hostname": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "ipAddress": {
                            "type": "ip"
                        },
                        "macAddress": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "eventType": {
                    "type": "string"
                },
                "room": {
                    "dynamic": "true",
                    "properties": {
                        "building": {
                            "type": "string"
                        },
                        "coordinates": {
                            "type": "geo_point"
                        },
                        "floor": {
                            "type": "string"
                        },
                        "roomNumber": {
                            "type": "string"
                        },
                        "room": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "timestamp": {
                    "type": "date",
                    "format": "dateOptionalTime",
                    "enabled": true,
                    "store": true
                }
            }
        }
    },
    "settings": {
        "index": {
            "number_of_shards": "3",
            "number_of_replicas": "1"
        }
    },
    "warmers": {}
}'