/* For license and copyright information please see the LEGAL file in the code repository */

package lamp_p

// Base on lamp switch mechanism,
type SwitchType uint64

const SwitchType_Unset SwitchType = 0
const (
	// ToggleSwitch or TriggerBased
	// it is on||off state switch
	SwitchType_Toggle = (1 << iota)

	// It provide light intensity
	SwitchType_Rotary

	// It need PushAndHold to continuously be on
	SwitchType_PushButton
)
