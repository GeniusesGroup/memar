/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GUICategories indicate the domain record data fields.
type GUICategories interface {
	CategoriesID() []cp.CategoryUUID //
	SaveTime() protocol.Time         //
	RequestID() urp.UserRequestUUID  //
}

type GUICategories_StorageServices interface {
	Save(gc GUICategories) (nv protocol.NumberOfVersion, err protocol.Error)

	Count() (nv protocol.NumberOfVersion, err protocol.Error)
	Get(vo protocol.VersionOffset) (gc GUICategories, nv protocol.NumberOfVersion, err protocol.Error)
}

// TODO::: cache strategy?? 1 day or what?
