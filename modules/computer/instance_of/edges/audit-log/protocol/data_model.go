/* For license and copyright information please see the LEGAL file in the code repository */

package al_p

import (
	log_p "memar/process/log/protocol"
)

type DataModel interface {
	log_p.Event
	// TODO::: other condition
}
