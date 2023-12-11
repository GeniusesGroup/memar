/* For license and copyright information please see the LEGAL file in the code repository */

package usacp

import (
	usp "org/modules/user-sexuality/protocol"
)

type DataModel interface {
	Sexuality() usp.Sexuality
	Count() Count
}
