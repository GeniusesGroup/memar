/* For license and copyright information please see the LEGAL file in the code repository */

package bot_p

import (
	user_p "org/modules/identity/user/protocol"
)

type Field_BotID interface {
	BotID() UUID
}

type UUID user_p.UUID
