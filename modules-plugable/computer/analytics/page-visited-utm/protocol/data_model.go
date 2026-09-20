/* For license and copyright information please see the LEGAL file in the code repository */

package utm_p

import (
	user_p "org/modules/identity/user/protocol"
)

// Urchin Tracking Module (UTM) parameters
// https://en.wikipedia.org/wiki/UTM_parameters
type DataModel interface {
	Field_UtmID
	user_p.Field_UserUUID

	MarketingUTM
}
