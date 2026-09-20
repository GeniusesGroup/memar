/* For license and copyright information please see the LEGAL file in the code repository */

package st_p

// Go programming language
type SaveTemperatureRequest struct {
	Temperature int64  `unit:"celsius"`
	PartID      uint16 // can be any part of thing(specific type) that catch temperature e.g. Evaporator income air, Evaporator suction line, ...
	// ThingID     [16]byte			service get it from connection
	// ThingType   uint32			don't need to store for each record and stream-processing units must get it from proper location.
}

func SaveTemperature(req SaveTemperatureRequest) {
	// Save data as time-series for requested thing
}

// TODO::: SaveTemperatureSDK call this service by near domain app (respect edge-computing)

type SavePressureRequest struct {
	Pressure int64  `unit:"bar"`
	PartID   uint16 // can be any part of thing(specific type) that catch temperature e.g. Evaporator suction pressure, ...
	// ThingID     [16]byte			service get it from connection
	// ThingType   uint32			don't need to store for each record and stream-processing units must get it from proper location.
}

func SavePressure(req SaveTemperatureRequest) {
	// Save data as time-series for requested thing
}

// TODO::: SavePressureSDK call this service by near domain app (respect edge-computing)
