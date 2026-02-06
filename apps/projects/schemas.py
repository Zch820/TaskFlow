from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.projects.serializers import ProjectSerializer, ProjectListSerializer


project_list_schema = (
    extend_schema(
        tags=["Projects"],
        summary="List projects",
        description="List all projects for the authenticated user",
        responses={
            200: OpenApiResponse(
                description="Paginated list of projects",
                response=ProjectListSerializer(many=True),
            ),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
)

project_create_schema = (
    extend_schema(
        tags=["Projects"],
        summary="Create project",
        description="Create a new project for the authenticated user",
        request=ProjectSerializer,
        responses={
            201: ProjectSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
)

project_retrieve_schema = (
    extend_schema(
        tags=["Projects"],
        summary="Retrieve project",
        description="Retrieving a project by ID",
        responses={
            200: ProjectSerializer,
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        },
    )
)

project_update_schema = (
    extend_schema(
        tags=["Projects"],
        summary="Update project",
        description="Update a project by ID",
        request=ProjectSerializer,
        responses={
            200: ProjectSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        },
    )
)

project_delete_schema = (
    extend_schema(
        tags=["Projects"],
        summary="Delete project",
        description="Soft-Delete a project by ID",
        responses={
            204: OpenApiResponse(description="Project soft-deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Project not found"),
        },
    )
)
