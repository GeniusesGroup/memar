/* For license and copyright information please see the LEGAL file in the code repository */

package prgp

import (
	request_p "memar/audit/request/protocol"
	project_p "org/modules/business/project/protocol"

	group_p "org/modules/organization/group/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	project_p.Field_ProjectID
	group_p.Field_GroupID
	ProjectGroupRelation() Type

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
