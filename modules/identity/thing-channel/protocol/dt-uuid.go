/* For license and copyright information please see the LEGAL file in the code repository */

package channel_p

import quiddity_p "org/modules/identity/quiddity/protocol"

type Field_ChannelID interface {
	// Typically one or more ports or channels are assigned to the device, each with a special purpose
	ChannelID() UUID
}

// It is quiddity identifier to let user assign `name` or `label` or `status` to each channel.
type UUID quiddity_p.UUID
