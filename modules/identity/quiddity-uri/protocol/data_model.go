/* For license and copyright information please see the LEGAL file in the code repository */

package qu_p

import (
	audit_p "org/modules/computer/audit/protocol"
	quiddity_p "org/modules/identity/quiddity/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
// https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
// https://en.wikipedia.org/wiki/Uniform_Resource_Name
// https://en.wikipedia.org/wiki/Electronic_Product_Code
type DataModel interface {
	Field_URI
	quiddity_p.Field_QuiddityID

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
