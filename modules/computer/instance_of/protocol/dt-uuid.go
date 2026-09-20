/* For license and copyright information please see the LEGAL file in the code repository */

package instance_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_InstanceUUID interface {
	InstanceID() UUID
}

// UUID as InstanceID or software(application) node instance
type UUID thing_p.UUID
