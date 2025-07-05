juce_add_plugin(MyPlugin
    COMPANY_NAME "MyAwesomeCompany"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE
    PLUGIN_MANUFACTURER_CODE Juce
    PLUGIN_CODE Plgn
    FORMATS VST3 AU Standalone
    PRODUCT_NAME "MyCMakePluginAttempt"
)

target_sources(MyPlugin
    PRIVATE
        PluginProcessor.cpp
        PluginEditor.cpp
        PluginProcessor.h
        PluginEditor.h
        DSP.cpp
)

target_compile_definitions(MyPlugin
    PRIVATE
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
)

target_link_libraries(MyPlugin
    PRIVATE
        juce::juce_audio_utils
        juce::juce_dsp
        juce::juce_gui_extra
)
