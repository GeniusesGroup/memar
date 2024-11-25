/* For license and copyright information please see the LEGAL file in the code repository */

package project_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_ProjectID interface {
	ProjectID() UUID
}

type UUID quiddity_p.UUID
