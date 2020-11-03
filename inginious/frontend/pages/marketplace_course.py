# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

""" Course page """
import web

from inginious.common.exceptions import ImportCourseException
from inginious.frontend.marketplace_courses import get_marketplace_course
from inginious.frontend.pages.marketplace import import_course
from inginious.frontend.pages.utils import INGIniousAuthPage


class MarketplaceCourse(INGIniousAuthPage):
    """ Course marketplace """

    def get_course(self, courseid):
        """ Return the course """
        try:
            course = get_marketplace_course(courseid)
        except:
            raise self.app.forbidden(message=_("Course unavailable."))

        return course

    def GET_AUTH(self, courseid):  # pylint: disable=arguments-differ
        """ GET request """
        # Change to teacher privilege when created
        if not self.user_manager.user_is_superadmin():
            raise self.app.forbidden(message=_("You're not allowed to do that"))

        course = self.get_course(courseid)
        return self.show_page(course)

    def POST_AUTH(self, courseid):  # pylint: disable=arguments-differ
        """ POST request """
        # Change to teacher privilege when created
        if not self.user_manager.user_is_superadmin():
            raise self.app.forbidden(message=_("You're not allowed to do that"))

        course = self.get_course(courseid)
        user_input = web.input()
        errors = []
        if "new_courseid" in user_input:
            new_courseid = user_input["new_courseid"]
            try:
                import_course(course, new_courseid, self.user_manager.session_username(), self.course_factory)
            except ImportCourseException as e:
                errors.append(str(e))
            if not errors:
                raise web.redirect(self.app.get_homepath() + "/admin/{}".format(new_courseid))
        return self.show_page(course, errors)

    def show_page(self, course, errors=None):
        """ Prepares and shows the course marketplace """
        if errors is None:
            errors = []

        return self.template_helper.render("marketplace_course.html", course=course, errors=errors)
