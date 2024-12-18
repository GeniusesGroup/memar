/* For license and copyright information please see the LEGAL file in the code repository */

package la_p

import (
	qsp "org/modules/identity/quiddity-status/protocol"
)

type Field_Status interface {
	Status() Status
}

type Status qsp.Quiddity_Status
