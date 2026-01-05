/* For license and copyright information please see the LEGAL file in the code repository */

package is_p

import (
	error_p "memar/error/protocol"

	ip "org/modules/financial/invoice/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(invoiceID ip.UUID) (dm DataModel, err error_p.Error)
}
