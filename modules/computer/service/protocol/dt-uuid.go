/* For license and copyright information please see the LEGAL file in the code repository */

package computer_service_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_ServiceID interface {
	BusinessServiceID() UUID
}

// Applications module service identifier e.g. Get(product), Register(content), ...
type UUID record_p.UUID
