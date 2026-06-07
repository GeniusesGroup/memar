/* For license and copyright information please see the LEGAL file in the code repository */

package rule_p

import (
	software_p "org/modules/computer/software/protocol"
	thing_p "org/modules/identity/thing/protocol"
)

type Model interface {
	thing_p.Model
	software_p.Model
}
