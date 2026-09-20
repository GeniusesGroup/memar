/* For license and copyright information please see the LEGAL file in the code repository */

package score_p

import (
	error_p "memar/process/error/protocol"

	user_p "org/modules/identity/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(userID user_p.UUID) (dm DataModel, err error_p.Error)
}
