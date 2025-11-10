"""
Code Snippets Library
Common Minecraft mod patterns and code snippets
"""

import customtkinter as ctk
import pyperclip
from typing import Dict, List

from config import THEME, LAYOUT


# Snippet library
SNIPPETS = {
    "Basic Mod": {
        "description": "Basic Forge mod structure",
        "language": "java",
        "code": '''@Mod("your_mod_id")
public class YourMod {
    public static final String MOD_ID = "your_mod_id";
    
    public YourMod(IEventBus modEventBus, ModContainer modContainer) {
        // Register setup method
        modEventBus.addListener(this::commonSetup);
        
        // Register ourselves for server events
        NeoForge.EVENT_BUS.register(this);
    }
    
    private void commonSetup(final FMLCommonSetupEvent event) {
        // Common setup code
    }
}'''
    },
    "Custom Item": {
        "description": "Create a custom item",
        "language": "java",
        "code": '''public class ModItems {
    public static final DeferredRegister<Item> ITEMS = 
        DeferredRegister.create(Registries.ITEM, YourMod.MOD_ID);
    
    public static final Supplier<Item> CUSTOM_ITEM = ITEMS.register("custom_item",
        () -> new Item(new Item.Properties()));
    
    public static void register(IEventBus eventBus) {
        ITEMS.register(eventBus);
    }
}'''
    },
    "Custom Block": {
        "description": "Create a custom block",
        "language": "java",
        "code": '''public class ModBlocks {
    public static final DeferredRegister<Block> BLOCKS = 
        DeferredRegister.create(Registries.BLOCK, YourMod.MOD_ID);
    
    public static final Supplier<Block> CUSTOM_BLOCK = BLOCKS.register("custom_block",
        () -> new Block(BlockBehaviour.Properties.of()
            .strength(3.0F, 3.0F)
            .sound(SoundType.STONE)));
    
    public static void register(IEventBus eventBus) {
        BLOCKS.register(eventBus);
    }
}'''
    },
    "Event Handler": {
        "description": "Handle game events",
        "language": "java",
        "code": '''@EventBusSubscriber(modid = YourMod.MOD_ID)
public class ModEvents {
    
    @SubscribeEvent
    public static void onPlayerJoin(PlayerEvent.PlayerLoggedInEvent event) {
        Player player = event.getEntity();
        player.sendSystemMessage(Component.literal("Welcome!"));
    }
    
    @SubscribeEvent
    public static void onBlockBreak(BlockEvent.BreakEvent event) {
        // Handle block break
    }
}'''
    },
    "Custom Command": {
        "description": "Create a custom command",
        "language": "java",
        "code": '''public class CustomCommand {
    public static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(Commands.literal("customcommand")
            .requires(source -> source.hasPermission(2))
            .executes(context -> {
                context.getSource().sendSuccess(
                    () -> Component.literal("Command executed!"),
                    true
                );
                return 1;
            })
        );
    }
}'''
    },
    "Capability": {
        "description": "Add custom data to entities",
        "language": "java",
        "code": '''public class ModCapabilities {
    public static final DeferredRegister<AttachmentType<?>> ATTACHMENT_TYPES = 
        DeferredRegister.create(Registries.ATTACHMENT_TYPE, YourMod.MOD_ID);
    
    public static final Supplier<AttachmentType<Integer>> CUSTOM_DATA = 
        ATTACHMENT_TYPES.register("custom_data", 
            () -> AttachmentType.builder(() -> 0).build());
    
    public static void register(IEventBus eventBus) {
        ATTACHMENT_TYPES.register(eventBus);
    }
}'''
    },
    "Recipe": {
        "description": "Create a custom recipe",
        "language": "java",
        "code": '''public class ModRecipes {
    public static final DeferredRegister<RecipeSerializer<?>> RECIPE_SERIALIZERS = 
        DeferredRegister.create(Registries.RECIPE_SERIALIZER, YourMod.MOD_ID);
    
    public static final Supplier<RecipeSerializer<CustomRecipe>> CUSTOM_RECIPE = 
        RECIPE_SERIALIZERS.register("custom_recipe",
            () -> new CustomRecipeSerializer());
    
    public static void register(IEventBus eventBus) {
        RECIPE_SERIALIZERS.register(eventBus);
    }
}'''
    },
    "GUI Screen": {
        "description": "Create a custom GUI screen",
        "language": "java",
        "code": '''public class CustomScreen extends Screen {
    public CustomScreen() {
        super(Component.literal("Custom Screen"));
    }
    
    @Override
    protected void init() {
        super.init();
        
        // Add buttons and widgets
        this.addRenderableWidget(Button.builder(
            Component.literal("Click me"),
            button -> {
                // Button clicked
            })
            .bounds(this.width / 2 - 100, this.height / 2 - 10, 200, 20)
            .build()
        );
    }
    
    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        this.renderBackground(graphics, mouseX, mouseY, partialTick);
        graphics.drawCenteredString(this.font, this.title, this.width / 2, 20, 0xFFFFFF);
        super.render(graphics, mouseX, mouseY, partialTick);
    }
}'''
    },
    "Packet Handler": {
        "description": "Handle network packets",
        "language": "java",
        "code": '''public class ModPackets {
    private static final String PROTOCOL_VERSION = "1";
    public static SimpleChannel INSTANCE;
    
    private static int packetId = 0;
    private static int id() {
        return packetId++;
    }
    
    public static void register() {
        INSTANCE = ChannelBuilder
            .named(ResourceLocation.fromNamespaceAndPath(YourMod.MOD_ID, "messages"))
            .networkProtocolVersion(1)
            .clientAcceptedVersions(Channel.VersionTest.exact(1))
            .serverAcceptedVersions(Channel.VersionTest.exact(1))
            .simpleChannel();
        
        INSTANCE.messageBuilder(CustomPacket.class, id())
            .encoder(CustomPacket::encode)
            .decoder(CustomPacket::decode)
            .consumerMainThread(CustomPacket::handle)
            .add();
    }
}'''
    },
    "Config File": {
        "description": "Create mod configuration",
        "language": "java",
        "code": '''public class ModConfig {
    public static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();
    public static final ForgeConfigSpec SPEC;
    
    public static final ForgeConfigSpec.ConfigValue<Integer> CUSTOM_VALUE;
    public static final ForgeConfigSpec.BooleanValue ENABLE_FEATURE;
    
    static {
        BUILDER.push("General Settings");
        
        CUSTOM_VALUE = BUILDER
            .comment("Custom configuration value")
            .defineInRange("customValue", 100, 0, 1000);
        
        ENABLE_FEATURE = BUILDER
            .comment("Enable custom feature")
            .define("enableFeature", true);
        
        BUILDER.pop();
        SPEC = BUILDER.build();
    }
}'''
    }
}


class SnippetsLibrary(ctk.CTkScrollableFrame):
    """
    Code snippets library.
    Fast access to common Minecraft patterns.
    """
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="💡 Code Snippets",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Search bar
        self.create_search_bar()
        
        # Snippets list
        self.create_snippets_list()
    
    def create_search_bar(self):
        """Create search bar"""
        search_frame = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        search_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search snippets...",
            font=THEME["font_body"],
            height=40
        )
        self.search_entry.pack(fill="x", padx=15, pady=15)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_snippets())
    
    def create_snippets_list(self):
        """Create snippets list"""
        self.snippets_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.snippets_frame.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Display all snippets
        for name, snippet in SNIPPETS.items():
            self.create_snippet_card(name, snippet)
    
    def create_snippet_card(self, name: str, snippet: Dict):
        """Create snippet card"""
        card = ctk.CTkFrame(
            self.snippets_frame,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        card.pack(fill="x", pady=5)
        
        # Header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=name,
            font=("Segoe UI", 16, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        name_label.pack(side="left")
        
        # Language badge
        ctk.CTkLabel(
            header_frame,
            text=snippet['language'].upper(),
            font=THEME["font_small"],
            text_color=THEME["accent"],
            fg_color=THEME["bg_primary"],
            corner_radius=4,
            padx=8,
            pady=2
        ).pack(side="right")
        
        # Description
        ctk.CTkLabel(
            card,
            text=snippet['description'],
            font=THEME["font_body"],
            text_color=THEME["text_secondary"],
            anchor="w"
        ).pack(fill="x", padx=20, pady=(0, 10))
        
        # Code preview (first few lines)
        code_lines = snippet['code'].split('\n')
        preview = '\n'.join(code_lines[:3]) + "\n..." if len(code_lines) > 3 else snippet['code']
        
        code_preview = ctk.CTkTextbox(
            card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_secondary"],
            font=THEME["font_code"],
            height=80,
            wrap="none"
        )
        code_preview.pack(fill="x", padx=20, pady=(0, 10))
        code_preview.insert("1.0", preview)
        code_preview.configure(state="disabled")
        
        # Buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkButton(
            button_frame,
            text="📋 Copy",
            width=100,
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"],
            command=lambda: self.copy_snippet(snippet['code'])
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="👁️ View Full",
            width=100,
            fg_color=THEME["card_hover"],
            command=lambda: self.view_full_snippet(name, snippet)
        ).pack(side="left", padx=5)
    
    def filter_snippets(self):
        """Filter snippets based on search"""
        search_text = self.search_entry.get().lower()
        
        # Clear current snippets
        for widget in self.snippets_frame.winfo_children():
            widget.destroy()
        
        # Show matching snippets
        for name, snippet in SNIPPETS.items():
            if (search_text in name.lower() or 
                search_text in snippet['description'].lower() or
                search_text in snippet['code'].lower()):
                self.create_snippet_card(name, snippet)
    
    def copy_snippet(self, code: str):
        """Copy snippet to clipboard"""
        try:
            pyperclip.copy(code)
            self.show_message("Copied to clipboard!", THEME["success"])
        except:
            # Fallback if pyperclip not available
            self.show_message("Could not copy (pyperclip not installed)", THEME["error"])
    
    def view_full_snippet(self, name: str, snippet: Dict):
        """View full snippet in modal"""
        modal = ctk.CTkToplevel(self)
        modal.title(name)
        modal.geometry("800x600")
        modal.transient(self)
        
        # Header
        header_frame = ctk.CTkFrame(modal, fg_color=THEME["card_bg"])
        header_frame.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header_frame,
            text=name,
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"]
        ).pack(side="left", padx=20, pady=15)
        
        ctk.CTkButton(
            header_frame,
            text="📋 Copy",
            width=100,
            fg_color=THEME["accent"],
            command=lambda: self.copy_snippet(snippet['code'])
        ).pack(side="right", padx=20, pady=15)
        
        # Description
        ctk.CTkLabel(
            modal,
            text=snippet['description'],
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(padx=20, pady=(10, 0))
        
        # Full code
        code_text = ctk.CTkTextbox(
            modal,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=THEME["font_code"],
            wrap="none"
        )
        code_text.pack(fill="both", expand=True, padx=20, pady=20)
        code_text.insert("1.0", snippet['code'])
        code_text.configure(state="disabled")
    
    def show_message(self, message: str, color: str):
        """Show temporary message"""
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            font=THEME["font_body"],
            text_color=color
        )
        msg_label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(3000, msg_label.destroy)

