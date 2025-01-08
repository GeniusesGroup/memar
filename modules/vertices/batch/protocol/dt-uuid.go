/* For license and copyright information please see the LEGAL file in the code repository */

package batch_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_BatchID interface {
	ProductBatchID() UUID
}

type UUID quiddity_p.UUID
