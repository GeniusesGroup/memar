/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// GUICategories indicate the domain record data fields.
type GUICategories interface {
	CategoriesID() [][16]byte   // quiddity domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type GUICategories_StorageServices interface {
	Save(gc GUICategories) (nv protocol.NumberOfVersion, err protocol.Error)

	Count() (nv protocol.NumberOfVersion, err protocol.Error)
	Get(vo protocol.VersionOffset) (gc GUICategories, nv protocol.NumberOfVersion, err protocol.Error)
}

// TODO::: cache strategy?? 1 day or what?
