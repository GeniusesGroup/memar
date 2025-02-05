/* For license and copyright information please see the LEGAL file in the code repository */

package estate_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_EstateID interface {
	EstateID() UUID
}

type Field_EstateIDs interface {
	EstateIDs() []UUID
}

// UUID use to identify any estate part like
// itself(sum of all), area, houses, buildings, buildings parts (e.g. apartment, ...), ...
// use in Coordinate domain too, to get physical location.
type UUID thing_p.UUID
