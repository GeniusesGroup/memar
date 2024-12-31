/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	text_p "org/modules/knowledge/text/protocol"
)

type Field_Terms interface {
	Terms() Terms
}

// HTML, CSS, JS base, Solidity PL is other option
type Terms text_p.UUID
