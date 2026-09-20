/* For license and copyright information please see the LEGAL file in the code repository */

package thing_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_ThingUUID interface {
	ThingUUID() UUID
}

type Field_ThingsUUID interface {
	ThingsUUID() []UUID
}

// It is the base identifier for any other domains.
// It will let users to assign `name` or `label` or `status` to each channel.
// UUID can be same with any other UUID domains e.g. user, ...
// It MUST be unique ID in all domains.
// Usually use to SET/GET and show locale title by knowledge/text domain.
type UUID record_p.UUID
