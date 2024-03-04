import React, { useEffect, useState } from 'react'
import { apiService } from '../../api'
import DeviceTable from './DeviceTable'

export default function Devices() {

  const [triggers, setTriggers] = useState([])
  const [targets, setTargets] = useState([])

  const getTargets = async () => {
    const data = await apiService.triggers.getTriggers()
    console.log(data)
    setTriggers(data)
  }

  const getTriggers = async () => {
    const data = await apiService.targets.getTargets()
    console.log(data)
    setTargets(data.map((trigger) => ({ ...trigger, id: trigger.matter_id })))
  }

  useEffect(() => {
    getTargets()
    getTriggers()
  }, [])

  return (
    <div style={{ display: 'flex', justifyContent: 'space-around' }}>
      <DeviceTable devices={triggers} />
      <DeviceTable devices={targets} />
    </div>
  )
}
