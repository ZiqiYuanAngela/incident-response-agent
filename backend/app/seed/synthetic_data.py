SERVICES = [
    {
        "name": "payment-service",
        "owner": "Payments Platform",
        "tier": 1,
    },
    {
        "name": "order-service",
        "owner": "Order Management",
        "tier": 1,
    },
    {
        "name": "notification-service",
        "owner": "Customer Communications",
        "tier": 2,
    },
]


HISTORICAL_INCIDENTS = [
    {
        "id": "INC-001",
        "service_name": "payment-service",
        "title": "Database connection pool exhaustion",
        "symptoms": [
            "database connection timeout",
            "connection pool utilization at 100%",
            "payment request latency",
        ],
        "root_cause": (
            "The database connection pool was too small for peak traffic."
        ),
        "resolution": (
            "Increased connection pool size and fixed connections that "
            "were not being released."
        ),
    },
    {
        "id": "INC-002",
        "service_name": "payment-service",
        "title": "Database driver regression",
        "symptoms": [
            "timeouts after deployment",
            "database connection failures",
            "elevated payment errors",
        ],
        "root_cause": (
            "A new database driver version changed connection timeout "
            "behavior."
        ),
        "resolution": "Rolled back the database driver upgrade.",
    },
    {
        "id": "INC-003",
        "service_name": "order-service",
        "title": "Redis cache saturation",
        "symptoms": [
            "redis timeout",
            "cache latency",
            "order retrieval failures",
        ],
        "root_cause": "Redis memory reached its configured maximum.",
        "resolution": "Evicted stale keys and increased Redis capacity.",
    },
]


RUNBOOKS = [
    {
        "id": "RB-001",
        "service_name": "payment-service",
        "title": "Database connectivity investigation",
        "keywords": [
            "database",
            "connection",
            "timeout",
            "pool",
        ],
        "steps": [
            "Check active, idle, and waiting database connections.",
            "Inspect connection pool utilization.",
            "Compare pool settings with the previous deployment.",
            "Check database response latency.",
        ],
    },
    {
        "id": "RB-002",
        "service_name": "payment-service",
        "title": "Deployment regression investigation",
        "keywords": [
            "deployment",
            "release",
            "regression",
            "rollback",
        ],
        "steps": [
            "Identify the first failing request after deployment.",
            "Compare changed dependencies and configuration.",
            "Review error rate before and after deployment.",
            "Prepare rollback criteria.",
        ],
    },
    {
        "id": "RB-003",
        "service_name": "order-service",
        "title": "Redis incident investigation",
        "keywords": ["redis", "cache", "memory", "timeout"],
        "steps": [
            "Check Redis memory utilization.",
            "Inspect cache hit rate and eviction count.",
            "Review slow commands.",
        ],
    },
]


DEPLOYMENTS = [
    {
        "id": "DEP-101",
        "service_name": "payment-service",
        "version": "2.4.0",
        "deployed_at": "2026-07-18T09:30:00Z",
        "changes": [
            "Upgraded database driver",
            "Changed database connection timeout",
        ],
    },
    {
        "id": "DEP-100",
        "service_name": "payment-service",
        "version": "2.3.9",
        "deployed_at": "2026-07-11T11:00:00Z",
        "changes": ["Updated request logging"],
    },
    {
        "id": "DEP-201",
        "service_name": "order-service",
        "version": "5.2.1",
        "deployed_at": "2026-07-17T14:00:00Z",
        "changes": ["Updated Redis client"],
    },
]