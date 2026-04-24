from uuid import UUID

from pydantic import BaseModel

from backend.db.dal import PagesDAL, PagesUpdate
from backend.db.externals import PagesPublicModel
from backend.route_handler.base import RouteHandler


class PageTextEditRequest(BaseModel):
    new_text: str


class PageResponse(PagesPublicModel):
    pass


class PageAPIHandler(RouteHandler):
    def register_routes(self) -> None:
        self.router.add_api_route(
            "/api/page/{page_id}/edit-text",
            self.page_edit_text,
            methods=["POST"],
            response_model=PageResponse,
        )

    async def page_edit_text(
        self,
        page_id: UUID,
        payload: PageTextEditRequest,
    ) -> PageResponse:
        async with self.app.db_session_factory.session() as db_session:
            updated_page = await PagesDAL.update_by_id(
                db_session, page_id, PagesUpdate(user_message=payload.new_text)
            )
            await db_session.commit()
            return PageResponse(
                **PagesPublicModel.model_validate(updated_page).model_dump()
            )
