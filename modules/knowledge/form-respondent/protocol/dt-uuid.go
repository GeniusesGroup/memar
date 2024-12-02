/* For license and copyright information please see the LEGAL file in the code repository */

package fr_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_FormRespondentID interface {
	FormRespondentID() UUID
}

type UUID quiddity_p.UUID
