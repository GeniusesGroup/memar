/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	software_p "org/modules/computer/software/protocol"
	widget_p "org/modules-plugable/computer/widget/protocol"
	user_p "org/modules/identity/user/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

// GUICategories indicate the domain record data fields.
type GUICategories interface {
	widget_p.Field_WidgetID
	software_p.Field_SoftwareID
	user_p.Field_UserUUID
	CategoriesID() []label_p.UUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}

// TODO::: cache strategy?? 1 day or what?
