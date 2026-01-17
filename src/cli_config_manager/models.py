from enum import Enum
from typing import Optional, Annotated
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    HttpUrl,
    field_validator,
    model_validator,
    ConfigDict
)


# -----------------------------------------------------------------------------
# Java 类比: Enum 定义
# public enum Role { ADMIN, EDITOR, VIEWER; }
# -----------------------------------------------------------------------------
class Role(str, Enum):
    """
    用户角色枚举。
    继承 str 使得该枚举在 JSON 序列化时自动表现为字符串，
    无需像 Java 那样编写自定义序列化器。
    """
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


# -----------------------------------------------------------------------------
# Java 类比: UserDTO with Bean Validation
# @Data @NoArgsConstructor
# public class User {... }
# -----------------------------------------------------------------------------
class User(BaseModel):
    """
    用户数据模型。
    继承 BaseModel 自动获得了构造函数、__str__、JSON 序列化等能力。
    """

    # -------------------------------------------------------------------------
    # Configuration (ConfigDict)
    # Java 类比: Jackson 的 @JsonIgnoreProperties 或 ObjectMapper 全局配置
    # str_strip_whitespace=True 相当于对所有 String 字段自动调用 trim()
    # -------------------------------------------------------------------------
    model_config = ConfigDict(
        str_strip_whitespace=True,
        frozen=False,  # 如果设为 True，对象创建后即不可变 (类似 Java Record)
        extra='ignore',  # 忽略输入数据中未定义的字段 (类似 @JsonIgnoreProperties(ignoreUnknown=true))
        json_schema_extra={
            "example": {
                "name": "张三",
                "email": "zhangsan@company.com",
                "age": 25,
                "website": "https://example.com",
                "role": "admin"
            }
        }
    )

    # Field: name
    # Java: @NotNull private String name;
    name: str = Field(
        min_length=1,
        max_length=50,
        description="用户姓名，长度在1-50个字符之间"
    )

    # Field: email
    # Java: @Email @NotNull private String email;
    # Pydantic 内置的 EmailStr 类型会自动进行正则和 DNS 格式校验
    email: EmailStr

    # Field: age
    # Java: @Min(18) @Max(100) private int age;
    # 使用 Annotated + Field 是 Pydantic V2 推荐的元数据附加方式
    age: Annotated[int, Field(
        ge=18,  # greater than or equal to
        le=100,  # less than or equal to
        description="用户年龄，必须在 18-100 之间"
    )]

    # Field: website
    # Java: @URL private String website;
    # Optional[HttpUrl] = None 表示该字段可为 null (None)，且默认值为 None
    website: Optional[HttpUrl] = Field(
        default=None,
        description="用户个人网站URL，必须是有效的HTTP/HTTPS URL"
    )

    # Field: role
    # Java: @NotNull private Role role;
    role: Role

    # -------------------------------------------------------------------------
    # 字段级验证器 (Field Validator)
    # Java 类比: 自定义注解 @CheckWebsiteScheme 或在 Setter 中检查
    # -------------------------------------------------------------------------
    @field_validator('website')
    @classmethod
    def check_website_scheme(cls, v: Optional[HttpUrl]) -> Optional[HttpUrl]:
        """业务逻辑
         1、如果用户没有提供网站（website=None），不验证，直接返回 None
         2、如果存在website 验证是否使用 http 或 https 协议。
        注意：虽然 HttpUrl 类型本身已经隐含了协议检查，但这里演示如何扩展逻辑。

        参数:
            cls: 类本身 (User.class)
            v: 待验证的值
        """
        # 必要的边界检查，避免在 None 上访问 .scheme 属性导致 AttributeError
        # Python 的短路求值可精简该逻辑代码
        if v is None:
            return v
        # Pydantic V2 中 HttpUrl 是一个对象，有 scheme 属性
        if v.scheme not in ['http', 'https']:
            raise ValueError('Website URL must use HTTP or HTTPS protocol')
        return v

    # -------------------------------------------------------------------------
    # 模型级验证器 (Model Validator) - 多字段联合校验
    # Java 类比: 类级别的自定义注解 @ValidUserLogic 或在 build() 方法中检查
    # mode='after' 表示在所有单字段验证通过后执行此逻辑
    # -------------------------------------------------------------------------
    @model_validator(mode='after')
    def check_admin_email_domain(self) -> 'User':
        """
        业务规则：如果角色是 Admin，邮箱必须以 @company.com 结尾。

        Java 实现通常需要在 Bean 上加 @AssertTrue 方法：
        @AssertTrue(message="...")
        public boolean isAdminEmailValid() {... }
        """
        # 在 'after' 模式下，self 已经是一个填充好数据的 User 实例
        if self.role == Role.ADMIN:
            # 需要将 EmailStr 转为 str 进行字符串操作
            if not str(self.email).endswith('@company.com'):
                raise ValueError('Admin users must have a corporate email (@company.com)')

        return self