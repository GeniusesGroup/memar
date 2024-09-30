/* For license and copyright information please see the LEGAL file in the code repository */

package qsp

import (
	audit_p "org/modules/computer/audit/protocol"
	quiddity_p "org/modules/identity/quiddity/protocol"
	text_p "org/modules/knowledge/text/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
// https://en.wikipedia.org/wiki/Structure
type DataModel interface {
	quiddity_p.Field_QuiddityID
	Ability() text_p.UUID
	Limitation() text_p.UUID

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
