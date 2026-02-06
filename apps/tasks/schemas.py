from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.tasks.serializers import TaskSerializer


task_list_schema = (
    extend_schema(
        tags=["Tasks"],
        summary="List tasks",
        description="List all tasks under a project for the authenticated user",
        responses={
            200: TaskSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
)

task_create_schema = (
    extend_schema(
        tags=["Tasks"],
        summary="Create task",
        description="Create a new task under a project for the authenticated user",
        request=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
)

task_retrieve_schema = (
    extend_schema(
        tags=["Tasks"],
        summary="Retrieve task",
        description="Retrieve a task by ID",
        responses={
            200: TaskSerializer,
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        },
    )
)

task_update_schema = (
    extend_schema(
        tags=["Tasks"],
        summary="Update task",
        description="Update a task by ID",
        request=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        },
    )
)

task_delete_schema = (
    extend_schema(
        tags=["Tasks"],
        summary="Delete task",
        description="Soft-Delete a task by ID",
        responses={
            204: OpenApiResponse(description="Task soft-deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Task not found"),
        },
    )
)
