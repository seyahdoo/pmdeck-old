package com.seyahdoo.pmdeck

class Event<T,Y> {
    private val handlers = arrayListOf<(Event<T,Y>.(T, Y) -> Unit)>()
    operator fun plusAssign(handler: Event<T,Y>.(T, Y) -> Unit) { handlers.add(handler) }
    operator fun invoke(value: T,value2: Y) { for (handler in handlers) handler(value,value2) }
}