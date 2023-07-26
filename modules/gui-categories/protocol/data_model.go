/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	cp "org/modules/category/protocol"
)

// GUICategories indicate the domain record data fields.
type GUICategories interface {
	CategoriesID() []cp.CategoryUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// TODO::: cache strategy?? 1 day or what?
