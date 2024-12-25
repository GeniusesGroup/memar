/* For license and copyright information please see the LEGAL file in the code repository */

package label

const (
	Status_Readys = (1 << iota)
	Status_Shutdown

	Status_DiskPressure
	Status_MemoryPressure
	Status_ProcessPressure
	Status_GPUPressure
	Status_TPUPressure
	Status_NetworkUnavailable
	// TODO::: add more status
)
