/* For license and copyright information please see the LEGAL file in the code repository */

package bs_p

import (
	service_p "memar/operation/service/protocol"
)

type Field_ServiceID interface {
	BusinessServiceID() ServiceUUID
}

// Applications module service identifier e.g. Get(product), Register(content), ...
type ServiceUUID service_p.ServiceID
