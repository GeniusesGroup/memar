/* For license and copyright information please see the LEGAL file in the code repository */

package batch_p

import (
	account_p "org/modules/economics/account/protocol"
)

type Field_BatchID interface {
	BatchID() UUID
}

// DC abbreviation for distribution-center or Warehouse
type UUID account_p.UUID
