/* For license and copyright information please see the LEGAL file in the code repository */

package hardware_p

import (
	device_p "org/modules/computer/device/protocol"
)

type Field_HardwareID interface {
	HardwareID() UUID
}

type UUID device_p.UUID
