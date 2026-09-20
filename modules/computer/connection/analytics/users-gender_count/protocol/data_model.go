/* For license and copyright information please see the LEGAL file in the code repository */

package ugac_p

import (
	gender_p "org/modules/identity/taxon/edges/gender/protocol"
)

type DataModel interface {
	gender_p.Field_GenderUUID
	Count() int64
}
